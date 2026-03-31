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
| Embeddings           | Gemini embeddings               |
| Vector Search        | Chroma Vector database          |
| Web Scraping         | BeautifulSoup                   |
