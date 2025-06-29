# workflows/main_flow.py

from langgraph.graph import StateGraph
from agents.product_manager import ProductManagerAgent
from agents.architect import ArchitectAgent
from llms.factory import get_llm
from typing import TypedDict

# ✅ Define the state shape
class AppState(TypedDict, total=False):
    user_prompt: str
    product_spec: str
    architecture_plan: str
    last_agent: str

def create_flow(model_name="llama3"):
    llm = get_llm(model_name)
    pm_agent = ProductManagerAgent(llm)
    arch_agent = ArchitectAgent(llm)

    def product_manager_node(state: AppState) -> AppState:
        result = pm_agent.run(state)
        return {**state, **result}

    def architect_node(state: AppState) -> AppState:
        result = arch_agent.run(state)
        return {**state, **result}

    builder = StateGraph(state_schema=AppState)
    builder.add_node("ProductManager", product_manager_node)
    builder.add_node("Architect", architect_node)

    builder.set_entry_point("ProductManager")
    builder.add_edge("ProductManager", "Architect")

    return builder.compile()