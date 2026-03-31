from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup


def load_data(url):
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=2,
        extractor=lambda html: BeautifulSoup(html, "html.parser").text
    )
    docs = loader.load()

    return docs
