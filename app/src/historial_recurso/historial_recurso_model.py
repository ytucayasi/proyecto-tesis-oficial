# historial_recurso_model.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from .historial_recurso_entity import EstadoRecurso

class HistorialRecursoBase(BaseModel):
    generacion_recurso_id: int = Field(..., description="ID de la generación de recurso")
    evaluacion_id: int = Field(..., description="ID de la evaluación")
    estado_recurso: EstadoRecurso = Field(
        default=EstadoRecurso.ACTIVO,
        description="Estado del recurso (activo/inactivo)"
    )
    fecha_generacion: Optional[datetime] = Field(
        default_factory=datetime.utcnow,
        description="Fecha de generación del recurso"
    )

    @validator('estado_recurso')
    def validate_estado(cls, v):
        if isinstance(v, str):
            return EstadoRecurso(v.lower())
        return v

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

class HistorialRecurso(HistorialRecursoBase):
    pass

class UpdateHistorialRecurso(BaseModel):
    estado_recurso: Optional[EstadoRecurso] = Field(
        None,
        description="Estado del recurso (activo/inactivo)"
    )
    fecha_generacion: Optional[datetime] = Field(
        None,
        description="Fecha de generación del recurso"
    )

    @validator('estado_recurso')
    def validate_estado(cls, v):
        if v is not None:
            if isinstance(v, str):
                return EstadoRecurso(v.lower())
        return v

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

class HistorialRecursoResponse(HistorialRecursoBase):
    historial_recurso_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }