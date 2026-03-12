import os
import shutil
from fastapi import FastAPI, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain_postgres import PGVector
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents.middleware import SummarizationMiddleware
from contextlib import asynccontextmanager
from tempfile import NamedTemporaryFile

POSTGRES_CONNECTION_STRING = (
    f"postgresql://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

PGVECTOR_CONNECTION_STRING = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB')}"
)


model = ChatOpenAI(model="gpt-4.1")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="docs",
    connection=PGVECTOR_CONNECTION_STRING,
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)


class ChatResponse(BaseModel):
    answer: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    with PostgresSaver.from_conn_string(POSTGRES_CONNECTION_STRING) as checkpointer:
        checkpointer.setup()

        app.state.agent = create_agent(
            model,
            tools=[],
            checkpointer=checkpointer,
            middleware=[
                SummarizationMiddleware(
                    model="gpt-4.1",
                    trigger=("tokens", 1000),
                    keep=("messages", 10)
                ),
                prompt_with_context
            ]
        )
        yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    last_query = request.state["messages"][-1].text

    retrieved_docs = vector_store.similarity_search(last_query)

    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    return (
        "You are a helpful assistant. Use the following context in your response:"
        f"\n\n{docs_content}"
    )


@app.post("/query", response_model=ChatResponse)
async def query(
    message: str = Form(),
    file: UploadFile | None = None
):
    agent = app.state.agent

    if file:
        if file.content_type != "application/pdf":
            raise HTTPException(400, "Only PDF files are supported.")

        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        try:
            loader = PyPDFLoader(tmp_path)
            docs = loader.load()
            chunks = text_splitter.split_documents(docs)

            vector_store.add_documents(chunks)
        finally:
            os.remove(tmp_path)

    result = agent.invoke(
        {"messages": [HumanMessage(content=message)]},
        {"configurable": {"thread_id": "1"}},
    )

    response = result["messages"][-1]

    return ChatResponse(answer=response.content)
