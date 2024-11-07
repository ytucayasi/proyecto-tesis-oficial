from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class EscuelaProfesionalBase(BaseModel):
    nivel_id: int
    facultad_id: int
    nombre: str
    codigo: str
    descripcion: Optional[str] = None
    estado: Optional[int] = Field(default=1)

class EscuelaProfesional(EscuelaProfesionalBase):
    pass

class UpdateEscuelaProfesional(BaseModel):
    nivel_id: Optional[int] = None
    facultad_id: Optional[int] = None
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[int] = None
