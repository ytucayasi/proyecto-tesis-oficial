from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum

class TipoReplicacionEnum(str, Enum):
    curso = "curso"
    plan = "plan"

class EquivalenciaReplicadas(BaseModel):
    curso_id: Optional[int] = None
    plan_academico_id: Optional[int] = None
    tipo_replicacion: TipoReplicacionEnum
    fecha_replicacion: date

class UpdateEquivalenciaReplicadas(BaseModel):
    curso_id: Optional[int] = None
    plan_academico_id: Optional[int] = None
    tipo_replicacion: Optional[TipoReplicacionEnum] = None
    fecha_replicacion: Optional[date] = None
