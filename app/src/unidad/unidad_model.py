from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UnidadBase(BaseModel):
    curso_id: int
    nombre: str
    resultado_aprendizaje: str
    descripcion: str

class Unidad(UnidadBase):
    pass

class UpdateUnidad(BaseModel):
    curso_id: Optional[int] = None
    nombre: Optional[str] = None
    resultado_aprendizaje: Optional[str] = None
    descripcion: Optional[str] = None

class UnidadResponse(UnidadBase):
    unidad_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True