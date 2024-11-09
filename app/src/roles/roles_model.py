from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Roles(BaseModel):
    nombre_rol: str
    descripcion: str
    estado: Optional[bool] = True

class UpdateRoles(BaseModel):
    nombre_rol: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[bool] = None
