from typing import TypedDict

class AppState(TypedDict, total=False):
    session_id: str
    user_prompt: str
    product_spec: str
    architecture_plan: str
    feedback: str
    last_agent: str