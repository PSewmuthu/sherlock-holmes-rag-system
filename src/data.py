from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore")


def clean_wiki_html(html: str) -> str:
    """Extracts only article body content and removes website boilerplate."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted elements (nav, sidebars, scripts, footers, headers)
    for element in soup([
        "script", "style", "header", "footer", "nav",
        "aside", "table", "div.mw-page-base", "div#vector-toc"
    ]):
        element.decompose()

    # Extract content from MediaWiki main content container if available
    content = soup.find(id="mw-content-text") or soup.find("main") or soup

    # Get clean text separated by linebreaks
    return content.get_text(separator="\n", strip=True)


def load_data(url):
    loader = RecursiveUrlLoader(
        url=url,
        max_depth=2,
        extractor=clean_wiki_html,
        prevent_outside=True  # Exclude common non-article media/meta paths on wikis
    )
    docs = loader.load()

    # Filter out empty or trivially short documents
    valid_docs = [doc for doc in docs if len(doc.page_content.strip()) > 20]
    return valid_docs


def split_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, separators=["\n\n", "\n", " ", ""])
    splits = text_splitter.split_documents(docs)

    return splits
