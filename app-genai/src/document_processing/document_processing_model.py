from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class DocumentProcessingResponse(BaseModel):
    summary: str
    file_path: str
    metadata: Dict[str, str]
    created_at: datetime

    class Config:
        orm_mode = True