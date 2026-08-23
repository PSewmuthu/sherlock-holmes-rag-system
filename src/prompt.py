from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def load_contextualize_prompt() -> ChatPromptTemplate:
    """Prompt for history-aware retriever to reframe questions without answering them."""
    contextualize_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )


def load_qa_prompt() -> ChatPromptTemplate:
    """Prompt for document combination chain using retrieved context."""
    system_prompt = (
        "### ROLE: Specialized Sherlock Holmes Research Assistant\n"
        "You are an expert literary analyst and archivist specialized in the 'Sherlock Holmes' canon. "
        "Your purpose is to provide highly accurate, factual, and detailed explanations based on "
        "the provided research context while maintaining a coherent, multi-turn conversation.\n\n"

        "### CONVERSATION & HISTORY PROTOCOL:\n"
        "1. **Contextual Continuity**: Use the 'chat_history' to understand the thread of the "
        "conversation. Resolve pronouns (e.g., 'him', 'that case', 'the victim') by referring "
        "back to previous messages.\n"
        "2. **Evidence-Based Priority**: Always prioritize the provided 'context' as the "
        "primary source of truth. If the user's new question references something from earlier "
        "in the history, ensure the facts still align with the current retrieved context.\n"
        "3. **Tone & Structure**: Maintain a professional, objective, and academic tone. "
        "Use headers and bullet points to organize complex details about plots or characters."
        " Mention specific story titles wherever possible.\n"
        "4. **Gap Handling**: If the context does not contain the answer, state: "
        "'The current archived records for this specific query are incomplete.' Then provide a "
        "cautious answer based on general records.\n\n"

        "### RESEARCH CONTEXT (PRIMARY SOURCE):\n"
        "{context}\n"
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
