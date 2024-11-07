from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Input(BaseModel):
    nombre: str
    link_archivo: str

class UpdateInput(BaseModel):
    nombre: Optional[str] = None
    link_archivo: Optional[str] = None

class InputResponse(BaseModel):
    input_id: int
    nombre: str
    link_archivo: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True