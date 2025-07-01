# agents/architect.py

from agents.base import Agent
from memory.vectorstore import save_to_memory
from utils.hitl import human_review

class ArchitectAgent(Agent):
    def run(self, state: dict) -> dict:
        prompt = self.build_prompt(state)
        output = self.llm.invoke(prompt)

        output, feedback = human_review(output, "Architect")
        if feedback:
            state["feedback"] = feedback  # Store feedback to adjust prompt
            return self.run(state)        # Regenerate using feedback

        if output:
            save_to_memory("Architect", output, metadata={"type": "architecture_plan"})
            return {
                "architecture_plan": output,
                "last_agent": "Architect"
            }

    def build_prompt(self, state: dict) -> str:
        base_prompt = f"""
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

        # Include feedback if present
        if "feedback" in state:
            base_prompt += f"\n\n💬 User Feedback on previous version:\n{state['feedback']}\n"

        return base_prompt