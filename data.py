from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup


def load_data(url):
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=2,
        extractor=lambda html: BeautifulSoup(html, "html.parser").text
    )
    docs = loader.load()

    return docs


def split_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, chunk_overlap=50)
    splits = text_splitter.split_documents(docs)

    return splits
