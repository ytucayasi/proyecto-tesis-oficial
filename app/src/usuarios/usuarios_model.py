from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class Usuarios(BaseModel):
    persona_id: int
    correo_electronico: EmailStr
    contrasena: str
    estado: Optional[bool] = True

class UpdateUsuarios(BaseModel):
    correo_electronico: Optional[EmailStr] = None
    contrasena: Optional[str] = None
    estado: Optional[bool] = None
