import json
from typing import List, Dict
import os

def extract_files_from_json_file(session_id: str, agent_name: str, doc_type: str, base_path: str = "output"):
    folder = os.path.join(base_path, session_id)
    os.makedirs(folder, exist_ok=True)

    filename = f"{agent_name}_{doc_type}.json"
    filepath = os.path.join(folder, filename)
    """
    Opens a JSON file, parses its contents, and extracts the list of files
    from the nested 'content' field.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        List[Dict[str, str]]: A list of dictionaries with 'path' and 'content' keys.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Now parse the nested 'content' string field
        content_data = json.loads(json_data['content'])
        
        return content_data.get('files', [])
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing JSON or extracting files: {e}")
        return []