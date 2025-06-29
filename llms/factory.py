# llms/factory.py
from langchain_ollama import OllamaLLM

def get_llm(model_name: str = "llama3"):
    return OllamaLLM(model=model_name)