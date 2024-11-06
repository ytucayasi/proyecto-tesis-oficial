from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NivelBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class Nivel(NivelBase):
    pass

class UpdateNivel(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
