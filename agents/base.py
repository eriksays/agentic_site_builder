# agents/base.py

class Agent:
    def __init__(self, llm):
        self.llm = llm

    def run(self, state: dict) -> dict:
        raise NotImplementedError("Agent must implement `run()`")