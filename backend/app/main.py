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
from langchain.messages import SystemMessage, HumanMessage
from langchain_postgres import PGVector
from tempfile import NamedTemporaryFile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatResponse(BaseModel):
    answer: str


model = ChatOpenAI(model="gpt-4.1")
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

CONNECTION_STRING = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

vector_store = PGVector(
    embeddings=embeddings,
    collection_name="docs",
    connection=CONNECTION_STRING,
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
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


agent = create_agent(model, tools=[], middleware=[prompt_with_context])


@app.post("/query", response_model=ChatResponse)
async def query(
    message: str = Form(),
    file: UploadFile | None = None
):
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

        result = agent.invoke({
            "messages": [
                HumanMessage(content=message)
            ]
        })

        response = result["messages"][-1]
    else:
        response = model.invoke([
            SystemMessage("You are a helpful assistant."),
            HumanMessage(content=message)
        ])

    return ChatResponse(answer=response.content)
