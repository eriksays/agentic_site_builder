# memory/vectorstore.py

from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings

def get_vectorstore(persist_dir="./chroma_store"):
    embedding_function = OllamaEmbeddings()
    return Chroma(persist_directory=persist_dir, embedding_function=embedding_function)