import os
import json
# You’ll add more agent imports here later
from agents.generic_agent import GenericAgent


def get_registered_agents_dynamically(llm):
    profiles_dir = os.path.join(os.path.dirname(__file__), "profiles")
    agents = []

    for filename in os.listdir(profiles_dir):
        if filename.endswith(".json"):
            with open(os.path.join(profiles_dir, filename), "r") as f:
                profile = json.load(f)
            if profile.get('enabled') == "True":
                #input(f"{profile.get('name')}, {profile.get('enabled')}")
                agents.append((profile.get("order", 9999), GenericAgent(llm, profile)))

    # Sort by 'order' and strip out the tuples
    sorted_agents = [agent for _, agent in sorted(agents, key=lambda x: x[0])]
    return sorted_agents