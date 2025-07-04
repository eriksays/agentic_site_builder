def format_context(context_docs: dict[str, str]) -> str:
    """
    Turn a dictionary like {"AgentName_doc_type": content} into a readable
    context string for use in prompts.
    """
    parts = []

    for key, text in context_docs.items():
        if "_" in key:
            agent, doc_type = key.split("_", 1)
            doc_type_clean = doc_type.replace("_", " ")
        else:
            agent = key
            doc_type_clean = "context"

        parts.append(f"[{agent}] provided {doc_type_clean}:\n{text.strip()}")

    return "\n\n".join(parts)