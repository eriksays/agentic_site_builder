# memory/vectorstore.py

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from config.settings import DEFAULT_MODEL

vectorstore = None

def get_vectorstore(persist_dir="./chroma_store"):
    global vectorstore
    if vectorstore is None:
        embeddings = OllamaEmbeddings(model=DEFAULT_MODEL)
        vectorstore = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vectorstore

def save_to_memory(agent_name: str, content: str, metadata: dict = {}):
    store = get_vectorstore()
    doc = Document(page_content=content, metadata={"agent": agent_name, **metadata})
    store.add_documents([doc])