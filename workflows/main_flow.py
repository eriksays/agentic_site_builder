from langgraph.graph import StateGraph
from typing import List
from agents.configurable_agent import load_agents_from_json
from memory.memory_store import MemoryStore
from workflows.state import AppState


def create_flow(agent_config_path: str, model_name: str, session_id: str, memory_store):
    # Load dynamic agents from JSON
    agents = load_agents_from_json(agent_config_path, model_name)

    # Build LangGraph flow with structured AppState
    builder = StateGraph(AppState)

    for agent in agents:
        builder.add_node(
            agent.name,
            lambda state, agent=agent: agent.run(
                state,
                session_id=session_id,
                memory_store=memory_store,
            ),
        )

    for i in range(len(agents) - 1):
        builder.add_edge(agents[i].name, agents[i + 1].name)

    builder.set_entry_point(agents[0].name)
    builder.set_finish_point(agents[-1].name)

    return builder.compile()