from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseAgent(ABC):
    def __init__(self, llm, name: str, input_keys: List[str], output_key: str, doc_type: str, persona: str):
        self.llm = llm
        self.name = name
        self.input_keys = input_keys
        self.output_key = output_key
        self.doc_type = doc_type  # For chroma storage
        self.persona = persona

    def run(self, state: Dict[str, Any], session_id: str, memory_store) -> Dict[str, Any]:
        # 1. Collect context
        context = memory_store.get_all_documents(session_id)
        inputs = [state[k] for k in self.input_keys if k in state]

        # 2. Generate output via LLM
        response = self._generate_response(inputs, context)

        # 3. Store output in memory
        memory_store.add_document(session_id, self.doc_type, response)

        # 4. Return state update
        return {self.output_key: response}

    @abstractmethod
    def _generate_response(self, inputs: List[str], context_docs: List[str]) -> str:
        ...