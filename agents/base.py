from abc import ABC, abstractmethod
from typing import List, Dict, Any
from utils.hitl import human_review
from utils.output_logger import save_agent_output


class BaseAgent(ABC):
    def __init__(self, llm, name: str, input_keys: List[str], output_key: str, doc_type: str, persona: str, enable_hitl: bool = True):
        self.llm = llm
        self.name = name
        self.input_keys = input_keys
        self.output_key = output_key
        self.doc_type = doc_type  # For chroma storage
        self.persona = persona
        self.enable_hitl = enable_hitl

    def run(self, state: Dict[str, Any], session_id: str, memory_store) -> Dict[str, Any]:
        #context_docs = memory_store.get_all_documents(session_id)
        context_docs = self.memory_store.get_all_documents(self.session_id)

        # ✅ Ensure inputs is a DICT
        inputs = {k: state[k] for k in self.input_keys if k in state}

        # ✅ Include feedback if available
        if "feedback" in state:
            inputs["feedback"] = state["feedback"]

        output = self._generate_response(inputs, context_docs)

        if self.enable_hitl:
            reviewed_output, feedback = human_review(output, self.name)
            if feedback:
                state["feedback"] = feedback
                return self.run(state, session_id, memory_store)
            output = reviewed_output
            # Save to disk
            save_agent_output(session_id, self.name, self.doc_type, output, approved=True, feedback=feedback)

        memory_store.add_document(session_id, self.doc_type, output)

        return {self.output_key: output}
    
    @classmethod
    def from_config(cls, config: Dict[str, Any], llm) -> "BaseAgent":
        return cls(
            llm=llm,
            name=config["name"],
            input_keys=config["input_keys"],
            output_key=config["output_key"],
            doc_type=config["doc_type"],
            persona=config["persona"],
            enable_hitl=config.get("enable_hitl", True)
        )

    def _generate_response(self, input_data):
        raise NotImplementedError("Subclasses or configurations must provide _generate_response.")