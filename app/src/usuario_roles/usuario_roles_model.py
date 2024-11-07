from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsuarioRoles(BaseModel):
    usuario_id: int
    rol_id: int

class UpdateUsuarioRoles(BaseModel):
    usuario_id: Optional[int] = None
    rol_id: Optional[int] = None
