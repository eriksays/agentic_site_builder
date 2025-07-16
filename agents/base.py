from abc import ABC, abstractmethod
from typing import List, Dict, Any
from utils.hitl import human_review
from utils.output_logger import save_agent_output
from utils.file_writer import write_code_files
from utils.get_content_from_json import extract_files_from_json_file
import json
import re
from pprint import pprint

class BaseAgent(ABC):
    def __init__(self, llm, name: str, output_key: str, doc_type: str, persona: str, enable_hitl: bool = False, writes_code: bool = False):
        self.llm = llm
        self.name = name
        self.output_key = output_key
        self.doc_type = doc_type  # For chroma storage
        self.persona = persona
        self.enable_hitl = False
        self.writes_code = writes_code

    def run(self, state: Dict[str, Any], session_id: str, memory_store) -> Dict[str, Any]:
        # ✅ Ensure inputs is a DICT
        inputs = {}

        # 1️⃣ On the very first invocation, if nothing is in memory, seed user_input
        raw = memory_store.get_all_documents(session_id)
        if not raw:
            # assumes your first agent’s inputs include "user_prompt"
            memory_store.add_document(session_id, "Client_user_input", state["user_prompt"])
            #TODO: add this to the output folder
            
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
        context_docs: Dict[str, str] = {}
        for i, item in enumerate(items):
            doc_type = item.metadata.get("doc_type")
            if not doc_type:
                print(f"[{self.name}] ⚠️ Missing 'doc_type' for document {i}, skipping.")
                continue
            context_docs[doc_type] = item.document

        # 🔍 Log what the agent is reviewing
        # TODO: add to a logging system instead of printing
        # print(f"\n[{self.name}] reviewing context documents:")
        # for k in context_docs:
        #     print(f" - {k}")
        # print()
 
        # 4️⃣ Generate this agent’s response with full context
        output = self._generate_response(state, context_docs, session_id)
 
         # Humanintheloop & logging…
         # ✅ Include feedback if available
        if "feedback" in state:
            inputs["feedback"] = state["feedback"]

        if self.enable_hitl:
            reviewed_output, feedback = human_review(output, self.name)
            if feedback:
                state["feedback"] = feedback
                return self.run(state, session_id, memory_store)
            output = reviewed_output
            
            #save to disk
            save_agent_output(session_id, self.name, self.doc_type, output, approved=True, feedback=feedback)
            if self.writes_code:
                # Try to extract the JSON block from inside the code fence
                
                files = extract_files_from_json_file(session_id, self.name, self.doc_type)
                
                write_code_files(session_id, self.name, self.doc_type, files)

                
        #TODO - we're not saving to output if enbale_hitl is set to false - need to fix that
        else:
            save_agent_output(session_id, self.name, self.doc_type, output, approved=True, feedback=None)
            if self.writes_code:
                # Try to extract the JSON block from inside the code fence
                files = extract_files_from_json_file(session_id, self.name, self.doc_type)
                
                write_code_files(session_id, self.name, self.doc_type, files)
        
        # 5️⃣ Persist this agent’s output under its doc_type
        memory_store.add_document(session_id, f'{self.name}_{self.doc_type}', output)
 
        return { self.output_key: output }

    @abstractmethod
    def _generate_response(self, inputs: List[str], context_docs: List[str]) -> str:
        ... 