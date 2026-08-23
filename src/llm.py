from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


def load_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    return llm


def load_embeddings():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview",
        max_retries=1
    )

    return embeddings
