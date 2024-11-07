from pydantic import BaseModel, Field
from typing import Optional

class CicloBase(BaseModel):
    programa_id: int
    nombre: str
    descripcion: Optional[str] = None
    numero_ciclo: int
    estado: Optional[int] = Field(default=1)

class Ciclo(CicloBase):
    pass

class UpdateCiclo(BaseModel):
    programa_id: Optional[int] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    numero_ciclo: Optional[int] = None
    estado: Optional[int] = None
