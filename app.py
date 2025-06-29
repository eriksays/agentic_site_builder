from config.settings import DEFAULT_MODEL, DEFAULT_APP
from llms.factory import get_llm
from workflows.main_flow import create_flow
from utils.input_with_default import input_with_default

if __name__ == "__main__":
    user_prompt = input_with_default("What kind of web app?", DEFAULT_APP)
    model_name = input_with_default("Ollama model to use", DEFAULT_MODEL)

    graph = create_flow(model_name=model_name)
    result = graph.invoke({"user_prompt": user_prompt})