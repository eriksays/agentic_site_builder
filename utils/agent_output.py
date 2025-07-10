from typing import TypedDict, Any, Optional

class AgentOutput(TypedDict, total=False):
    agent: str                  # Agent name (e.g. "ProductManagerAgent")
    doc_type: str               # Type of document produced (e.g. "product_spec")
    approved: bool              # Whether this output was approved by a human (optional)
    timestamp: str              # ISO 8601 format string (e.g. "2025-07-08T14:45:00Z")
    content: dict[str, Any]     # Actual structured content payload
    feedback: Optional[str]     # Optional user or system feedback
