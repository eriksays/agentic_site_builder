# memory/vectorstore.py

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from config.settings import DEFAULT_MODEL

from typing import Optional


class VectorStore:
    def __init__(self, persist_dir="./chroma_store", model_name=DEFAULT_MODEL):
        embeddings = OllamaEmbeddings(model=model_name)
        self.chroma = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

    def _make_key(self, session_id: str, doc_type: str) -> str:
        return f"{session_id}:{doc_type}"

    def add_document(self, session_id: str, doc_type: str, content: str):
        key = self._make_key(session_id, doc_type)
        self.chroma.add_texts(
            texts=[content],
            metadatas=[{"session_id": session_id, "doc_type": doc_type}],
            ids=[key]
        )

    def get_document(self, session_id: str, doc_type: str) -> Optional[str]:
        key = self._make_key(session_id, doc_type)
        results = self.chroma.get(ids=[key])
        if results and results['documents']:
            return results['documents'][0]
        return None

    def get_all_documents(self, session_id: str) -> list[str]:
        results = self.chroma.similarity_search(
            "project context",
            k=20,
            filter={"session_id": session_id}
        )
        return [doc.page_content for doc in results] if results else []