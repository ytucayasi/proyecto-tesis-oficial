from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Input(BaseModel):
    link_archivo: str

class UpdateInput(BaseModel):
    link_archivo: Optional[str] = None

class InputResponse(BaseModel):
    input_id: int
    link_archivo: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True