def input_with_default(prompt, default):
    full_prompt = f"{prompt} [{default}]: "
    response = input(full_prompt)
    return response.strip() or default