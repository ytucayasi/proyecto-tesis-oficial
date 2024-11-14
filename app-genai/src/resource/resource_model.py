from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .resource_entity import TipoRecurso

class ResourceBase(BaseModel):
    input_url: str
    titulo: str
    modelo: str
    diseno: int
    cantidad_paginas: int
    tipo_recurso: TipoRecurso
    url_recurso: str

class Resource(ResourceBase):
    pass

class UpdateResource(BaseModel):
    input_url: Optional[str] = None
    titulo: Optional[str] = None
    modelo: Optional[str] = None
    diseno: Optional[int] = None
    cantidad_paginas: Optional[int] = None
    tipo_recurso: Optional[TipoRecurso] = None
    url_recurso: Optional[str] = None

class ResourceResponse(ResourceBase):
    resource_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True