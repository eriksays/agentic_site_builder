from agents.product_manager import ProductManagerAgent
from agents.architect import ArchitectAgent
from agents.ux_designer import UXDesignerAgent
# You’ll add more agent imports here later



def get_registered_agents(llm):
    return [
        ProductManagerAgent(llm),
        ArchitectAgent(llm),
        UXDesignerAgent(llm),
        # Add BackendEngineerAgent(llm), etc. as you create them
    ]