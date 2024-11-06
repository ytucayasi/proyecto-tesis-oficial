from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class EstadoRecursosEnum(str, Enum):
    completo = "completo"
    parcial = "parcial"
    ninguno = "ninguno"

class EstadoEvaluacionEnum(str, Enum):
    pendiente = "pendiente"
    evaluado = "evaluado"
    asignacion_p = "asignacion_p"
    regeneracion_p = "regeneracion_p"

class CursoBase(BaseModel):
    nombre: str
    estado_recursos: EstadoRecursosEnum
    estado_evaluacion: EstadoEvaluacionEnum
    credito: int
    duracion_horas: int
    descripcion: Optional[str] = None

class Curso(CursoBase):
    pass

class UpdateCurso(BaseModel):
    nombre: Optional[str] = None
    estado_recursos: Optional[EstadoRecursosEnum] = None
    estado_evaluacion: Optional[EstadoEvaluacionEnum] = None
    credito: Optional[int] = None
    duracion_horas: Optional[int] = None
    descripcion: Optional[str] = None
