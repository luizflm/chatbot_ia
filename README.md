# 🤖 RAG AI Chatbot with Short-Term Memory

A full-stack Retrieval-Augmented Generation (RAG) chatbot that allows users to chat with their PDF documents. The system features persistent short-term memory, automatic conversation summarization, and a modern, responsive interface.

## 🌟 Key Features

* **PDF Analysis (RAG):** Upload PDFs and ask specific questions about their content.
* **Conversational Memory:** Powered by `LangGraph` and `PostgresSaver`, the bot remembers previous interactions within a specific thread.
* **Smart Summarization:** Integrated `SummarizationMiddleware` automatically condenses long histories to stay within token limits.
* **Vector Search:** Utilizes `pgvector` for efficient semantic search of document chunks.
* **Modern UI:** A clean, Tailwind-powered Vue.js interface with real-time typing indicators and auto-scrolling.
* **Fully Dockerized:** Seamless deployment with a single command.

---

## 🏗️ Tech Stack

### Backend
* **FastAPI:** High-performance Python API framework.
* **LangChain & LangGraph:** Orchestration for AI agents and memory persistence.
* **OpenAI GPT-4:** The brain of the assistant.
* **PGVector:** Vector database extension for PostgreSQL.

### Frontend
* **Vue.js 3:** Composition API with `<script setup>`.
* **Tailwind CSS:** Modern utility-first styling.
* **Axios:** For handling multi-part form data (PDF + Text) queries.

### Infrastructure
* **Docker & Docker Compose:** Containerization for backend, frontend, and database.
* **PostgreSQL:** Relational storage for both chat history and vector embeddings.

---

## 🚀 Getting Started

### Prerequisites
* Docker and Docker Compose installed.
* An OpenAI API Key.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/luizflm/chatbot_ia.git
    cd chatbot_ia
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the `./backend` directory (ensure this matches your `docker-compose.yml` path):
    ```env
    OPENAI_API_KEY=your_openai_key_here
    POSTGRES_USER=chatbot
    POSTGRES_PASSWORD=chatbot
    POSTGRES_DB=chatbot_db
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    ```

3.  **Launch the Application:**
    ```bash
    docker compose up --build
    ```

4.  **Access the services:**
    * **Frontend:** `http://localhost:8080`
    * **Backend API:** `http://localhost:8000`
    * **API Docs (Swagger):** `http://localhost:8000/docs`

---
