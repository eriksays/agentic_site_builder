# agents/product_manager.py

from agents.base import Agent

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
        return {
            "product_spec": output,
            "last_agent": "ProductManager"
        }