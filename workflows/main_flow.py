from langgraph.graph import StateGraph
from typing import TypedDict, List
from agents.base import BaseAgent


class AppState(TypedDict, total=False):
    session_id: str
    user_prompt: str
    product_spec: str
    architecture_plan: str

def create_flow(agents: List[BaseAgent], memory_store, session_id: str):
    builder = StateGraph(AppState)

    for agent in agents:
        builder.add_node(agent.name, lambda state, agent=agent: agent.run(state, session_id=session_id, memory_store=memory_store))

    for i in range(len(agents)-1):
        builder.add_edge(agents[i].name, agents[i+1].name)

    builder.set_entry_point(agents[0].name)
    builder.set_finish_point(agents[-1].name)

    return builder.compile()