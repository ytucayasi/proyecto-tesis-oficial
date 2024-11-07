from pydantic import BaseModel
from typing import Optional
from datetime import date

class FacultadBase(BaseModel):
    nombre: str
    codigo: str
    descripcion: str
    estado: str

class Facultad(FacultadBase):
    pass

class UpdateFacultad(BaseModel):
    nombre: Optional[str] = None
    codigo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None