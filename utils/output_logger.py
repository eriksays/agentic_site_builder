import os
from datetime import datetime
import json

def save_agent_output(session_id: str, agent_name: str, doc_type: str, content: str, approved=True, feedback=None, base_path: str = "output"):
    folder = os.path.join(base_path, session_id)
    os.makedirs(folder, exist_ok=True)

    #filename = f"{doc_type or agent_name}.json"
    filename = f"{agent_name}.json"
    file_path = os.path.join(folder, filename)

    data = {
        "agent": agent_name,
        "doc_type": doc_type,
        "approved": approved,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "content": content,
        "feedback": feedback,
    }

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

def save_metadata(session_id: str, metadata: dict, base_path: str = "output"):
    folder = os.path.join(base_path, session_id)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "metadata.json")

    import json
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2)