from pydantic import BaseModel

class ResourceGenerationRequest(BaseModel):
    titulo: str
    modelo: str
    diseno: int
    tipo_recurso: str
    cantidad_paginas: int

class ResourceGenerationResponse(BaseModel):
    resource_id: int
    summary_path: str
    resource_path: str

    class Config:
        orm_mode = True