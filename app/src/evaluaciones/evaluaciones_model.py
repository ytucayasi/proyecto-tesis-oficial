from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import date
from enum import Enum

class EvaluadoEnum(str, Enum):
    si = "si"
    no = "no"

class CalidadEnum(str, Enum):
    satisfactoria = "satisfactoria"
    negativa = "negativa"

class Evaluaciones(BaseModel):
    curso_id: int
    usuario_id: int
    comentarios: str
    fecha_evaluacion: date
    evaluado: EvaluadoEnum
    calidad: CalidadEnum
    calificacion: condecimal(max_digits=3, decimal_places=2)

class UpdateEvaluaciones(BaseModel):
    comentarios: Optional[str] = None
    fecha_evaluacion: Optional[date] = None
    evaluado: Optional[EvaluadoEnum] = None
    calidad: Optional[CalidadEnum] = None
    calificacion: Optional[condecimal(max_digits=3, decimal_places=2)] = None
