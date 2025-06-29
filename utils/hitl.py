# utils/hitl.py

def human_review(output: str, agent_name: str) -> tuple[str, str | None]:
    print(f"\n--- {agent_name} Output ---")
    print(output)
    while True:
        choice = input("Approve output? (y = yes, n = revise with feedback").strip().lower()
        if choice == "y":
            return output, None
        elif choice == "n":
            feedback = input("Enter feedback for improvement: ")
            return None, feedback
        