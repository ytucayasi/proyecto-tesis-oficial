from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
from .secuencia_aprendizaje_entity import EstadoRecursos

class SecuenciaAprendizajeBase(BaseModel):
    sesion_aprendizaje_id: int
    tipo_secuencia_id: int
    link_recurso: Optional[str] = None
    link_rubrica: Optional[str] = None
    estado_recursos: EstadoRecursos = EstadoRecursos.NINGUNO

class SecuenciaAprendizaje(SecuenciaAprendizajeBase):
    pass

class UpdateSecuenciaAprendizaje(BaseModel):
    sesion_aprendizaje_id: Optional[int] = None
    tipo_secuencia_id: Optional[int] = None
    link_recurso: Optional[str] = None
    link_rubrica: Optional[str] = None
    estado_recursos: Optional[EstadoRecursos] = None

class SecuenciaAprendizajeResponse(SecuenciaAprendizajeBase):
    secuencia_aprendizaje_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True