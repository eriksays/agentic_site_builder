from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents.registry import get_registered_agents_dynamically
from memory.vectorstore import VectorStore
from workflows.main_flow import create_flow
from llms.factory import get_llm
from fastapi.responses import JSONResponse
import uuid
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS setup for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WorkflowRequest(BaseModel):
    prompt: str
    model_name: str = "llama3"
    session_id: str | None = None

class StartAgentFlowRequest(BaseModel):
    projectName: str
    prompt: str
    model: str

@app.post("/run_workflow/")
def run_workflow(req: WorkflowRequest):
    # Generate or use session_id
    session_id = req.session_id or str(uuid.uuid4())

    # Setup everything
    llm = get_llm(req.model_name)
    memory_store = VectorStore()
    agents = get_registered_agents_dynamically(llm)
    graph = create_flow(agents, memory_store, session_id)

    # Run flow
    state = graph.invoke({"user_prompt": req.prompt})
    
    return {
        "session_id": session_id,
        "prompt": req.prompt,
        "output_state": state
    }

@app.post("/start-agent-flow")
async def start_agent_flow(request: StartAgentFlowRequest):
    session_id = str(uuid.uuid4())
    return JSONResponse(content={
        "sessionId": session_id,
        "received": {
            "projectName": request.projectName,
            "prompt": request.prompt,
            "model": request.model
        }
    })