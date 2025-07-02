from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents.registry import get_registered_agents
from memory.vectorstore import VectorStore
from workflows.main_flow import create_flow
from llms.factory import get_llm
import uuid

app = FastAPI()

class WorkflowRequest(BaseModel):
    prompt: str
    model_name: str = "llama3"
    session_id: str | None = None

@app.post("/run_workflow/")
def run_workflow(req: WorkflowRequest):
    # Generate or use session_id
    session_id = req.session_id or str(uuid.uuid4())

    # Setup everything
    llm = get_llm(req.model_name)
    memory_store = VectorStore()
    agents = get_registered_agents(llm)
    graph = create_flow(agents, memory_store, session_id)

    # Run flow
    state = graph.invoke({"user_prompt": req.prompt})
    
    return {
        "session_id": session_id,
        "prompt": req.prompt,
        "output_state": state
    }