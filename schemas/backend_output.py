from pydantic import BaseModel
from typing import List, Optional

class CodeFile(BaseModel):
    path: str
    content: str

class BackendOutput(BaseModel):
    files: List[CodeFile]
    summary: Optional[str] = None