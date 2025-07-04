import os

def log_prompt_and_response(agent_name: str, session_id: str, prompt: str, response: str):
    """
    Logs the prompt and response for an agent to logs/{session_id}/{agent_name}_*.txt
    """
    log_dir = os.path.join("logs", session_id)
    os.makedirs(log_dir, exist_ok=True)

    prompt_file = os.path.join(log_dir, f"{agent_name}_prompt.txt")
    response_file = os.path.join(log_dir, f"{agent_name}_response.txt")

    with open(prompt_file, "w", encoding="utf-8") as f:
        f.write(prompt)

    with open(response_file, "w", encoding="utf-8") as f:
        f.write(response)