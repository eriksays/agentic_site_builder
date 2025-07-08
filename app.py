from config.settings import DEFAULT_MODEL, DEFAULT_APP
from llms.factory import get_llm
from agents.registry import get_registered_agents, get_registered_agents_dynamically
from memory.vectorstore import VectorStore
from workflows.main_flow import create_flow
from utils.input_with_default import input_with_default
from utils.output_logger import save_metadata
from datetime import datetime
import uuid
from pprint import pprint

# Placeholder: use your actual chroma client
from chromadb import Client
chroma = Client()
memory_store = VectorStore()

if __name__ == "__main__":
    user_prompt = input_with_default("What kind of web app?", DEFAULT_APP)
    model_name = input_with_default("Ollama model to use", DEFAULT_MODEL)
    session_id = str(uuid.uuid4())  # Or allow manual entry for replayability

    # Setup components
    llm = get_llm(model_name)
    #agents = get_registered_agents(llm)

    agents = get_registered_agents_dynamically(llm)

    for agent in agents:
        print(f"Registered agent: {agent.name} ({agent.doc_type})")
        pprint(agent)
    
    graph = create_flow(agents, memory_store, session_id)

    # seed the raw user input
    memory_store.add_document(session_id, "Client_user_input", user_prompt)

    # Run flow
    result = graph.invoke({"user_prompt": user_prompt})
    save_metadata(session_id, {
        "timestamp": datetime.now().isoformat(),
        "model": model_name,
        "user_prompt": user_prompt
    })

    print(result)
    