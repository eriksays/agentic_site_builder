# memory/memory_store.py
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings  # Replace if needed

class MemoryStore:
    def __init__(self, persist_directory="chroma_store"):
        self.chroma = Chroma(
            collection_name="agent_memory",
            embedding_function=OpenAIEmbeddings(),
            persist_directory=persist_directory
        )

    def add_document(self, session_id: str, content: str, metadata: dict = None):
        if metadata is None:
            metadata = {}
        metadata["session_id"] = session_id
        self.chroma.add_texts([content], metadatas=[metadata])

    def get_all_documents(self, session_id: str):
        results = self.chroma.query(
            query_texts=[""],
            n_results=100,
            where={"session_id": session_id}
        )
        return results["documents"]

memory_store = MemoryStore()