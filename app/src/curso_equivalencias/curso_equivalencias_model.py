from pydantic import BaseModel
from typing import Optional
from datetime import date

class CursoEquivalencias(BaseModel):
    curso_id: int
    curso_equivalencia_id_fk: int
    tipo_equivalencia: str
    fecha_equivalencia: date

class UpdateCursoEquivalencias(BaseModel):
    tipo_equivalencia: Optional[str] = None
    fecha_equivalencia: Optional[date] = None
