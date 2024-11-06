from pydantic import BaseModel
from typing import Optional

class Users(BaseModel):
    name: str

class UpdateUser(BaseModel):
    name: Optional[str] = None