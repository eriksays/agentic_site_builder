# agents/architect.py

from agents.base import Agent
from memory.vectorstore import save_to_memory
from utils.hitl import human_review

class ArchitectAgent(Agent):
    def run(self, state: dict) -> dict:
        prompt = f"""
You are a senior Laravel architect.

Based on the following product spec, generate:
- A MySQL database schema (tables + fields, described or in SQL)
- A suggested Laravel file/folder structure using Blade + Livewire
- A list of web routes (e.g., GET /recipes, POST /login)

📌 Stack:
- Backend: Laravel (PHP)
- Frontend: Blade templates
- Interactivity: Alpine.js + Livewire
- Database: MySQL

---
PRODUCT SPEC:
{state.get('product_spec')}
"""
        output = self.llm.invoke(prompt)

        # 🧠 Human approval loop
        output = human_review(output, "Architect")
        if output is None:
            return self.run(state)  # Rerun agent if rejected

        # 💾 Save to Chroma vector DB
        # 🧠 Human approval loop
        output = human_review(output, "Architect")
        if output is None:
            return self.run(state)  # Rerun agent if rejected

        # 💾 Save to Chroma vector DB
        save_to_memory("Architect", output, metadata={"type": "architecture_plan"})


        return {
            "architecture_plan": output,
            "last_agent": "Architect"
        }