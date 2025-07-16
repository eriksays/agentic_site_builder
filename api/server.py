from fastapi import FastAPI, Request
from pydantic import BaseModel
from agents.registry import get_registered_agents_dynamically
from memory.vectorstore import VectorStore
from workflows.main_flow import create_flow
from llms.factory import get_llm
from fastapi.responses import JSONResponse
import uuid
from fastapi.middleware.cors import CORSMiddleware
from api.session_store import save_session, load_session
from agents.utils import get_agent_by_name
import time


app = FastAPI()

# CORS setup for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StepInput(BaseModel):
    session_id: str
    feedback: dict | None = None
    approve: bool = True

class WorkflowRequest(BaseModel):
    prompt: str
    model_name: str = "llama3"
    session_id: str | None = None

class StartAgentFlowRequest(BaseModel):
    projectName: str
    prompt: str
    model: str

'''
#don't use this endpoint, use /start-agent-flow instead
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
'''

@app.post("/start-agent-flow")
async def start_agent_flow(request: StartAgentFlowRequest):
    session_id = str(uuid.uuid4())
    
    session_data = initialize_session(
        session_id=session_id,
        prompt=request.prompt,
        project_name=request.projectName,
        model=request.model
    )
    
    # Save initial session state
    save_session(session_id, session_data)

    # Run first agent
    result = run_current_agent(session_data)

    

    return JSONResponse(content={
        "sessionId": session_id,
        "output": result
    })

@app.get("/agent-step")
async def get_current_agent_step(session_id: str):
    session = load_session(session_id)
    index = session["current_agent_index"]
    current_agent = session["agents"][index]
    output = session["outputs"].get(current_agent)

    return {
        "agent": current_agent,
        "output": output,
        "awaiting_feedback": output is not None and session["status"] == "waiting_for_feedback",
        "is_complete": session["status"] == "complete"
    }

@app.post("/agent-step")
async def post_next_agent_step(input: StepInput):
    session = load_session(input.session_id)
    
    index = session["current_agent_index"] + 1
    

    if session["status"] == "complete":
        return {"message": "Session complete"}

    current_agent_name = session["agents"][index]
    agent = get_agent_by_name(current_agent_name, session["model"])

    # Apply feedback if any (optional)
    if input.feedback:
        # Update memory, prompt, or inject changes
        pass

    # Run the agent
    memory_store = VectorStore(session["session_id"])
    result = agent.run({"user_prompt": session["prompt"]}, session_id=session["session_id"], memory_store=memory_store)

    session["outputs"][current_agent_name] = result

    if getattr(agent, "hitl_enabled", True) and input.approve is not False:
        session["status"] = "waiting_for_feedback"
    else:
        session["current_agent_index"] += 1
        if session["current_agent_index"] >= len(session["agents"]):
            session["status"] = "complete"
        else:
            session["status"] = "running"

    save_session(input.session_id, session)

    return JSONResponse(
        content=
        {
            "message": "Step complete", 
            "agent": current_agent_name,
            "session_id": input.session_id,
            "output": result
        }
    )


#--------------------
# internal logic helpers
# --------------------

def initialize_session(session_id, prompt, project_name, model):
    llm = get_llm(model)
    agents = get_registered_agents_dynamically(llm)

    return {
        "session_id": session_id,
        "prompt": prompt,
        "project_name": project_name,
        "model": model,
        "agents": [a.name for a in agents],
        "current_agent_index": 0,
        "outputs": {},
        "status": "running"
    }

def run_current_agent(session):

    agent_name = session["agents"][session["current_agent_index"]]
    agent = get_agent_by_name(agent_name, session["model"])
    memory_store = VectorStore(session["session_id"])
    result = agent.run({"user_prompt": session["prompt"]}, session_id=session["session_id"], memory_store=memory_store)
    session["outputs"][agent_name] = result

    if getattr(agent, "hitl_enabled", True):
        session["status"] = "waiting_for_feedback"
    else:
        session["current_agent_index"] += 1
        session["status"] = "complete" if session["current_agent_index"] >= len(session["agents"]) else "running"

    return result