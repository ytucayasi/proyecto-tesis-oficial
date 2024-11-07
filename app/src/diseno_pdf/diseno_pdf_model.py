from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .diseno_pdf_entity import EstadoDiseno

class DisenoPdfBase(BaseModel):
    nombre: str
    link_archivo: str
    estado: EstadoDiseno = EstadoDiseno.ACTIVO

class DisenoPdf(DisenoPdfBase):
    pass

class UpdateDisenoPdf(BaseModel):
    nombre: Optional[str] = None
    link_archivo: Optional[str] = None
    estado: Optional[EstadoDiseno] = None

class DisenoPdfResponse(DisenoPdfBase):
    diseno_pdf_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True