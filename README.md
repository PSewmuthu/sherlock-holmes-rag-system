# Sherlock Holmes RAG System 🕵️‍♂️🔍

## 🚀 Project Overview

Developed an **AI-powered Retrieval-Augmented Generation (RAG) system** that enables users to ask natural language questions about the original Sherlock Holmes stories written by Arthur Conan Doyle.

The system automatically retrieves relevant information from the **62 original Sherlock Holmes stories** and generates accurate answers using a large language model.

The stories were collected from the Arthur Conan Doyle Encyclopedia website and processed into vector embeddings to enable efficient semantic search.

A **FastAPI-based REST API** was developed to provide programmatic access to the AI system.

---

## 🌟 Key Features

### Data Collection

- Scraped the **62 Sherlock Holmes stories** from the Arthur Conan Doyle Encyclopedia website.
- Cleaned and structured the text for downstream processing.

---

### Retrieval-Augmented Generation (RAG)

Implemented a complete **RAG pipeline using LangChain**.

Pipeline stages:

1. Document ingestion
2. Text chunking
3. Embedding generation
4. Vector similarity search
5. Context-aware response generation

This approach allows the system to generate answers **based on real story content instead of hallucinating responses**.

---

### Large Language Model Integration

Integrated **Google Gemini free-tier models** for response generation.

The LLM receives:

- The user query
- Retrieved relevant story passages

It then produces **context-aware answers grounded in the original texts**.

---

### Semantic Search

The system converts story text into embeddings and stores them in a vector store, enabling:

- Semantic similarity search
- Context retrieval
- Accurate question answering

Example queries:

- “Who is Irene Adler?”
- “Which story introduces Professor Moriarty?”
- “How does Sherlock Holmes deduce the thief in The Blue Carbuncle?”

---

### FastAPI REST API

Developed a backend API using **FastAPI**.

Example endpoint:

POST /api/ask

Request:

```json
{
	"session_id": "your session id from /api/get_session_id",
	"question": "Who is Professor Moriarty?"
}
```

Response:

```json
{
	"answer": "Professor Moriarty is Sherlock Holmes' greatest enemy..."
}
```

This allows easy integration with:

- Web applications
- Chatbots
- Mobile apps

---

## System Architecture

```
User Query
     │
     ▼
FastAPI API
     │
     ▼
LangChain RAG Pipeline
     │
     ├── Vector Store (Embeddings)
     │
     ├── Retriever (Semantic Search)
     │
     ▼
Relevant Story Chunks
     │
     ▼
Gemini LLM
     │
     ▼
Generated Answer
```

---

## Technology Stack

| Component            | Technology                      |
| -------------------- | ------------------------------- |
| Backend API          | FastAPI                         |
| RAG Framework        | LangChain                       |
| LLM                  | Gemini                          |
| Programming Language | Python                          |
| Data Source          | Arthur Conan Doyle Encyclopedia |
| Embeddings           | HuggingFace embeddings          |
| Vector Search        | Chroma Vector database          |
| Web Scraping         | BeautifulSoup                   |
| Frontend UI          | Streamlit                       |

---

## 🏁 Getting Started

### Installation

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/pasindusewmuthu/sherlock-holmes-rag-system.git
    cd sherlock-holmes-rag-system
    ```

2.  **Configure Environment Variables & Secrets**

    Copy the example environment file and add your Google AI Studio key:

    ```bash
    cp .env.example .env
    ```

    Then collect your API key from [Google AI Studio](https://aistudio.google.com/api-keys) and update the .env file.

    ```bash
    GEMINI_API_KEY=your_google_ai_studio_key_here
    ```

    _(Optional)_ Configure local Streamlit Secrets:

    Create a .streamlit folder and add a secrets.toml file to specify your local or cloud API URL:

    ```bash
    mkdir .streamlit
    ```

    Add the following content to .streamlit/secrets.toml:

    ```bash
    API_BASE_URL="http://localhost:8000"
    ```

3.  **Start the Detective**:

    Running both the backend API and the frontend UI requires opening two separate terminal windows.

    Terminal 1: Start the FastAPI Backend

    ```bash
    uv run fastapi run main.py
    ```

    _Note: For the first run, it will take some time to download the embedding model and setup the vector database._

    Terminal 2: Start the Streamlit Frontend

    ```bash
    uv run streamlit run streamlit_app.py
    ```

## 📖 Example Queries

- _"What were the three distinctive features of the client in 'The Red-Headed League'?"_
- _"Compare the military background of Dr. Watson across different stories."_
- _"List all cases where Sherlock Holmes was forced to break the law to solve the mystery."_
