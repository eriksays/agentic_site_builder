# agents/product_manager.py

from agents.base import Agent
from memory.vectorstore import save_to_memory
from utils.hitl import human_review

class ProductManagerAgent(Agent):
    def run(self, state: dict) -> dict:
        prompt = self.build_prompt(state)
        output = self.llm.invoke(prompt)

        output, feedback = human_review(output, "Product Manager")
        if feedback:
            state["feedback"] = feedback  # Store feedback for rerun
            return self.run(state)        # Regenerate with new prompt

        if output:
            save_to_memory("ProductManager", output, metadata={"type": "product_spec"})
            return {
                "product_spec": output,
                "last_agent": "ProductManager"
            }

    def build_prompt(self, state: dict) -> str:
        base_prompt = f"""
You are a product manager. Based on the user's idea, define:

- A short product spec
- 3 user stories
- Suggested tech stack

📌 Use the following preferred technologies when possible:
- Backend: Laravel (PHP)
- Frontend: Blade templates (not React or Vue)
- Interactivity: Alpine.js for lightweight behavior, Livewire for backend-driven components
- Database: MySQL

---
USER IDEA:
{state.get('user_prompt')}
"""

        # Add feedback if present
        if "feedback" in state:
            base_prompt += f"\n\n💬 User Feedback on previous version:\n{state['feedback']}\n"

        return base_prompt