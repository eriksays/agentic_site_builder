import os
import json
from agents.product_manager import ProductManagerAgent
from agents.architect import ArchitectAgent
from agents.ux_designer import UXDesignerAgent
from agents.frontend_developer import FrontEndDeveloperAgent
from agents.backend_developer import BackEndDeveloperAgent
# You’ll add more agent imports here later
from agents.generic_agent import GenericAgent



def get_registered_agents(llm):
    return [
        #ProductManagerAgent(llm),
        #ArchitectAgent(llm),
        #UXDesignerAgent(llm),
        #BackEndDeveloperAgent(llm),
        FrontEndDeveloperAgent(llm),
        # Add BackendEngineerAgent(llm), etc. as you create them
    ]

def get_registered_agents_dynamically(llm):
    profiles_dir = os.path.join(os.path.dirname(__file__), "profiles")
    agents = []

    for filename in os.listdir(profiles_dir):
        if filename.endswith(".json"):
            with open(os.path.join(profiles_dir, filename), "r") as f:
                profile = json.load(f)
            agents.append((profile.get("order", 9999), GenericAgent(llm, profile)))

    # Sort by 'order' and strip out the tuples
    sorted_agents = [agent for _, agent in sorted(agents, key=lambda x: x[0])]
    return sorted_agents