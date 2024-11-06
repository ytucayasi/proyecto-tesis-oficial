from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ProgramaBase(BaseModel):
    plan_academico_id: int
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[int] = Field(default=1)
    fecha_inicio: date
    fecha_fin: Optional[date] = None

class Programa(ProgramaBase):
    pass

class UpdatePrograma(BaseModel):
    plan_academico_id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[int] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
