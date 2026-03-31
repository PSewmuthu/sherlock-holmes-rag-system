from fastapi import FastAPI
from chain import chain_init

app = FastAPI(
    title="Sherlock Holmes RAG API",
    description="An API that provides detailed, context-aware answers about Sherlock Holmes stories using a Retrieval-Augmented Generation (RAG) approach.",
    version="1.0.0"
)
