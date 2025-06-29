# agents/architect.py

from agents.base import Agent

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
        return {
            "architecture_plan": output,
            "last_agent": "Architect"
        }