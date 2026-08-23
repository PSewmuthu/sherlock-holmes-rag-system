from fastapi import FastAPI, HTTPException, status
from src.models import AskRequest
from src.chain import chain_init
from src.logger import logging
import uuid

app = FastAPI(
    title="Sherlock Holmes RAG API",
    description="An API that provides detailed, context-aware answers about Sherlock Holmes stories using a Retrieval-Augmented Generation (RAG) approach.",
    version="1.0.0"
)

logging.info("Initializing the RAG chain...")

rag_chain = chain_init()

logging.info("RAG chain initialized successfully")


@app.get("/api/get_session_id")
async def get_session_id():
    session_id = str(uuid.uuid4())
    logging.info(f"Generated new session ID: {session_id}")
    return {"session_id": session_id}


@app.post("/api/ask")
async def ask_question(request: AskRequest):
    question = request.question
    session_id = request.session_id
    logging.info(f"Processing question for session {session_id}")

    try:
        response = await rag_chain.ainvoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        )

        logging.info(
            f"Generated answer for session {session_id}")

        return {"answer": response["answer"]}
    except Exception as e:
        logging.error(
            f"Error processing question for session {session_id}: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your question. Please try again later."
        )
