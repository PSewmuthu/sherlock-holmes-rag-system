from fastapi import FastAPI, HTTPException, status
from chain import chain_init
from logger import logging

app = FastAPI(
    title="Sherlock Holmes RAG API",
    description="An API that provides detailed, context-aware answers about Sherlock Holmes stories using a Retrieval-Augmented Generation (RAG) approach.",
    version="1.0.0"
)

logging.info("Initializing the RAG chain...")

rag_chain = chain_init()

logging.info("RAG chain initialized successfully")


@app.post("/api/ask")
async def ask_question(question: str, session_id: str):
    logging.info(f"Processing question for session {session_id}: {question}")

    try:
        response = await rag_chain.invoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        )

        logging.info(
            f"Generated answer for session {session_id}: {response['answer']}")

        return {"answer": response["answer"]}
    except Exception as e:
        logging.error(
            f"Error processing question for session {session_id}: {str(e)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your question. Please try again later."
        )
