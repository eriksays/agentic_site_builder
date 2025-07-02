from config.settings import DEFAULT_MODEL, DEFAULT_APP
from llms.factory import get_llm
from agents.registry import get_registered_agents
from memory.vectorstore import VectorStore
from workflows.main_flow import create_flow
from utils.input_with_default import input_with_default
import uuid

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
    agents = get_registered_agents(llm)
    graph = create_flow(agents, memory_store, session_id)

    # Run flow
    result = graph.invoke({"user_prompt": user_prompt})
    print(result)