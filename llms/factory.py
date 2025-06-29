# llms/factory.py
from langchain_ollama import OllamaLLM
from config.settings import DEFAULT_MODEL

def get_llm(model_name: str = DEFAULT_MODEL):
    return OllamaLLM(model=model_name)
