# app.py

from workflows.main_flow import create_flow

def input_with_default(prompt, default):
    full_prompt = f"{prompt} [{default}]: "
    response = input(full_prompt)
    return response.strip() or default

if __name__ == "__main__":
    
    user_prompt = input_with_default(
        "What kind of web app do you want to build?",
        "A recipe site where users can submit, search, and favorite soup recipes"
    )

    graph = create_flow()
    result = graph.invoke({"user_prompt": user_prompt})
    
    print("\n--- Product Spec ---")
    print(result["product_spec"])