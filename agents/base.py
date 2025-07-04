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
        # ✅ Ensure inputs is a DICT
        inputs = {k: state[k] for k in self.input_keys if k in state}

        # 1️⃣ On the very first invocation, if nothing is in memory, seed user_input
        raw = memory_store.get_all_documents(session_id)
        if not raw:
            # assumes your first agent’s inputs include "user_prompt"
            memory_store.add_document(session_id, "user_input", state["user_prompt"])
            raw = memory_store.get_all_documents(session_id)

        # 2️⃣ Normalize Chroma’s return vs. a raw list
        from types import SimpleNamespace
        items = []
        if isinstance(raw, dict):
            # Chroma .get() style: { "documents": [...], "metadatas": [...], "ids": [...] }
            docs   = raw.get("documents", [])
            metas  = raw.get("metadatas", [])
            for doc, meta in zip(docs, metas):
                items.append(SimpleNamespace(document=doc, metadata=meta or {}))
        elif isinstance(raw, list):
            # Could be list of plain strings or of objects with .document/.metadata
            for entry in raw:
                if isinstance(entry, str):
                    items.append(SimpleNamespace(document=entry, metadata={}))
                elif hasattr(entry, "document") and hasattr(entry, "metadata"):
                    items.append(entry)

        # 3️⃣ Build a mapping: doc_type → text
        context_docs: Dict[str, str] = {
            item.metadata.get("doc_type", f"doc_{i}"): item.document
            for i, item in enumerate(items)
        }
 
        # 4️⃣ Generate this agent’s response with full context
        output = self._generate_response(state, context_docs)
 
         # Humanintheloop & logging…
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
            #save to disk
            save_agent_output(session_id, self.name, self.doc_type, output, approved=True, feedback=feedback)
 
        # 5️⃣ Persist this agent’s output under its doc_type
        memory_store.add_document(session_id, self.doc_type, output)
 
        return { self.output_key: output }

    @abstractmethod
    def _generate_response(self, inputs: List[str], context_docs: List[str]) -> str:
        ... 