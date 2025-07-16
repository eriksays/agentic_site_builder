# session_store.py

import os, json

SESSION_DIR = "sessions"

os.makedirs(SESSION_DIR, exist_ok=True)

def get_session_path(session_id):
    return os.path.join(SESSION_DIR, f"{session_id}.json")

def save_session(session_id, data):
    with open(get_session_path(session_id), "w") as f:
        json.dump(data, f)

def load_session(session_id):
    path = get_session_path(session_id)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Session {session_id} not found")
    with open(path, "r") as f:
        return json.load(f)