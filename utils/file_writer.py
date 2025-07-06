import os

def write_code_files(session_id: str, files: list[dict]):
    base_path = f"generated/{session_id}"
    for file in files:
        full_path = os.path.join(base_path, file["path"])
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(file["content"])