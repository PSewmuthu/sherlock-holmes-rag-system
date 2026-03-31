from langchain_chroma import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_classic.chains import create_history_aware_retriever
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from llm import load_llm, load_embeddings
from data import load_data, split_docs
from prompt import load_prompt

store = {}  # Store for session histories, keyed by session_id


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def chain_init():
    llm = load_llm()
    embedding_model = load_embeddings()
    docs = load_data(
        "https://www.arthur-conan-doyle.com/wiki/The_62_Sherlock_Holmes_stories_written_by_Arthur_Conan_Doyle")
    splits = split_docs(docs)

    vectorstore = Chroma.from_documents(
        documents=splits, embedding=embedding_model)
    retriever = vectorstore.as_retriever()

    prompt = load_prompt()

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, prompt
    )

    qa_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer"
    )

    return conversational_rag_chain
