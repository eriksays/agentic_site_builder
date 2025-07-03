from config.settings import DEFAULT_MODEL, DEFAULT_APP
from llms.factory import get_llm
from memory.memory_store import memory_store
from workflows.main_flow import create_flow
from utils.input_with_default import input_with_default
from utils.output_logger import save_metadata
from datetime import datetime
import uuid

if __name__ == "__main__":
    user_prompt = input_with_default("What kind of web app?", DEFAULT_APP)
    model_name = input_with_default("Ollama model to use", DEFAULT_MODEL)
    session_id = str(uuid.uuid4())  # Or allow manual entry for replayability

    # Setup components
    llm = get_llm(model_name)
    agent_config_path = "config/agents/"  # Directory containing JSON agent definitions
    # Build graph with dynamic agents (llm is passed internally)
    graph = create_flow(agent_config_path=agent_config_path, model_name=model_name, session_id=session_id, memory_store=memory_store)
    result = graph.invoke({"user_prompt": user_prompt, "session_id": session_id})

  
    save_metadata(session_id, {
        "timestamp": datetime.now().isoformat(),
        "model": model_name,
        "user_prompt": user_prompt
    })
    print(result)