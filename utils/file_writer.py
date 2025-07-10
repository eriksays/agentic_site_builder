import os
import codecs

def write_code_files(session_id: str, agent_name, doc_type, files: list[dict]):
    base_path = f"generated/{session_id}/{agent_name}/{doc_type}"
    for file in files:
        # Remove any leading slashes to ensure relative paths
        rel_path = file["path"].lstrip("/")
        full_path = os.path.join(base_path, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        content = file["content"].encode('utf-8').decode('unicode_escape')
        with open(full_path, "w") as f:
            f.write(content)