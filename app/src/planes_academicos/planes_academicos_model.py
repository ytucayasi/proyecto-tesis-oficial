from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PlanAcademicoBase(BaseModel):
    escuela_profesional_id: int
    nombre: str
    anio_inicio: date
    anio_fin: Optional[date] = None
    descripcion: Optional[str] = None
    estado: Optional[int] = Field(default=1)
    creditos_totales: Optional[int] = None

class PlanAcademico(PlanAcademicoBase):
    pass

class UpdatePlanAcademico(BaseModel):
    escuela_profesional_id: Optional[int] = None
    nombre: Optional[str] = None
    anio_inicio: Optional[date] = None
    anio_fin: Optional[date] = None
    descripcion: Optional[str] = None
    estado: Optional[int] = None
    creditos_totales: Optional[int] = None
