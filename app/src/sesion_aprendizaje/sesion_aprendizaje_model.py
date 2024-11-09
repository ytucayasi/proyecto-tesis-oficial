from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class SesionAprendizajeBase(BaseModel):
    unidad_id: int
    tema: str
    fecha_dictado: date
    numero_sesion: int

class SesionAprendizaje(SesionAprendizajeBase):
    pass

class UpdateSesionAprendizaje(BaseModel):
    unidad_id: Optional[int] = None
    tema: Optional[str] = None
    fecha_dictado: Optional[date] = None
    numero_sesion: Optional[int] = None

class SesionAprendizajeResponse(SesionAprendizajeBase):
    sesion_aprendizaje_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True