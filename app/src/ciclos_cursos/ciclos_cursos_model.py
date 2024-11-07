from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CicloCursoBase(BaseModel):
    ciclo_id: int
    curso_id: int

class CicloCurso(CicloCursoBase):
    pass

class UpdateCicloCurso(BaseModel):
    ciclo_id: Optional[int] = None
    curso_id: Optional[int] = None
