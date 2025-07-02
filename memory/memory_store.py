# memory/memory_store.py

from typing import Optional

class MemoryStore:
    def __init__(self, chroma_client):
        self.chroma = chroma_client  # Assume this is a chromadb.Collection or wrapper

    def _make_key(self, session_id: str, doc_type: str) -> str:
        return f"{session_id}:{doc_type}"

    def add_document(self, session_id: str, doc_type: str, content: str):
        key = self._make_key(session_id, doc_type)
        self.chroma.add(
            documents=[content],
            ids=[key],
            metadatas=[{"session_id": session_id, "doc_type": doc_type}]
        )

    def get_document(self, session_id: str, doc_type: str) -> Optional[str]:
        key = self._make_key(session_id, doc_type)
        results = self.chroma.get(ids=[key])
        if results and results['documents']:
            return results['documents'][0]
        return None

    def get_all_documents(self, session_id: str) -> list[str]:
        results = self.chroma.query(
            query_texts=["project context"],
            n_results=20,
            where={"session_id": session_id}
        )
        return results["documents"] if results else []