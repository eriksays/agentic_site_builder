# agents/utils.py

from agents.registry import get_registered_agents_dynamically
from llms.factory import get_llm

def get_agent_by_name(name: str, model: str):
    llm = get_llm(model)
    agents = get_registered_agents_dynamically(llm)
    for agent in agents:
        if agent.name == name:
            return agent
    raise ValueError(f"Agent '{name}' not found")