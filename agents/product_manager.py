# agents/product_manager.py

from agents.base import Agent
from memory.vectorstore import save_to_memory
from utils.hitl import human_review

class ProductManagerAgent(Agent):
    def run(self, state: dict) -> dict:
        prompt = f"""
        You are a product manager. Based on the user's idea, define:

        - A short product spec
        - 3 user stories
        - Suggested tech stack

        📌 Use the following preferred technologies when possible:
        - Backend: Laravel (PHP)
        - Frontend: Blade templates (not React or Vue)
        - Interactivity: Alpine.js for lightweight dynamic behavior, and Livewire for backend-driven interactivity (forms, modals, etc.)
        - Database: MySQL

        Design your recommendations to align with a progressive enhancement strategy, avoiding full SPA frameworks. All code and architecture should reflect a server-rendered app with enhanced interactivity using Alpine.js and Livewire.

        USER IDEA:
        {state['user_prompt']}
        """
        output = self.llm.invoke(prompt)
        output = human_review(output, "ProductManager")
        if output is None:
            return self.run(state)  # Rerun agent if rejected

        # 💾 Save to Chroma vector DB
        save_to_memory("ProductManager", output, {"type": "product_spec"})
    
        return {
            "product_spec": output,
            "last_agent": "ProductManager"
        }