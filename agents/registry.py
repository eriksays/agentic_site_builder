from agents.product_manager import ProductManagerAgent
from agents.architect import ArchitectAgent
# You’ll add more agent imports here later

def get_registered_agents(llm):
    return [
        ProductManagerAgent(llm),
        ArchitectAgent(llm),
        # Add BackendEngineerAgent(llm), etc. as you create them
    ]