# generacion_recurso_model.py
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from .generacion_recurso_entity import TipoDocumento

class GeneracionRecursoBase(BaseModel):
    input_id: int = Field(..., description="ID del input")
    diseno_id: int = Field(..., description="ID del diseño")
    numero_paginas: int = Field(..., ge=1, description="Número de páginas")
    tipo_documento: TipoDocumento = Field(..., description="Tipo de documento (word, pdf, ppt)")
    link_archivo: str

    @validator('tipo_documento')
    def lowercase_tipo_documento(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

    class Config:
        use_enum_values = True

class GeneracionRecurso(GeneracionRecursoBase):
    pass

class UpdateGeneracionRecurso(BaseModel):
    input_id: Optional[int] = None
    diseno_id: Optional[int] = None
    numero_paginas: Optional[int] = Field(None, ge=1)
    tipo_documento: Optional[TipoDocumento] = None
    link_archivo: Optional[str] = None

    @validator('tipo_documento')
    def lowercase_tipo_documento(cls, v):
        if isinstance(v, str):
            return v.lower()
        return v

    class Config:
        use_enum_values = True

class GeneracionRecursoResponse(GeneracionRecursoBase):
    generacion_recurso_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True