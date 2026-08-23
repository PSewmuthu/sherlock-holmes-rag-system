import os
from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_classic.chains import create_history_aware_retriever
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from .llm import load_llm, load_embeddings
from .data import load_data, split_docs
from .prompt import load_contextualize_prompt, load_qa_prompt

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(ROOT_DIR, "db")

store = {}  # Store for session histories, keyed by session_id


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def chain_init():
    llm = load_llm()
    embedding_model = load_embeddings()

    if os.path.exists(DB_DIR):
        vectorstore = Chroma(
            persist_directory=DB_DIR,
            embedding_function=embedding_model
        )
    else:
        docs = load_data(
            "https://www.arthur-conan-doyle.com/wiki/The_62_Sherlock_Holmes_stories_written_by_Arthur_Conan_Doyle"
        )
        splits = split_docs(docs)

        os.makedirs(DB_DIR, exist_ok=True)

        vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embedding_model,
            persist_directory=DB_DIR
        )

    retriever = vectorstore.as_retriever()

    # Load prompts separately
    contextualize_prompt = load_contextualize_prompt()
    qa_prompt = load_qa_prompt()

    # Pass the query rephrasing prompt (NO {context}) to retriever
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_prompt
    )

    # Pass the full QA prompt (WITH {context}) to document chain
    qa_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    return conversational_rag_chain
