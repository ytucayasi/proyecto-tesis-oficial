from src.config import config
from sqlalchemy import Integer, ForeignKey, Text, Date, Enum, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.historial_recurso.historial_recurso_entity import HistorialRecursoEntity

class EvaluadoEnum(PyEnum):
    si = "si"
    no = "no"

class CalidadEnum(PyEnum):
    satisfactoria = "satisfactoria"
    negativa = "negativa"

class Evaluaciones(config.Base):
    __tablename__ = "evaluaciones"

    evaluar_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curso_id: Mapped[int] = mapped_column(Integer)
    usuario_id: Mapped[int] = mapped_column(Integer)
    comentarios: Mapped[str] = mapped_column(Text)
    fecha_evaluacion: Mapped[datetime] = mapped_column(Date)
    evaluado: Mapped[EvaluadoEnum] = mapped_column(Enum(EvaluadoEnum))
    calidad: Mapped[CalidadEnum] = mapped_column(Enum(CalidadEnum))
    calificacion: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con HistorialRecurso
    historiales: Mapped[List["HistorialRecursoEntity"]] = relationship(
        "HistorialRecursoEntity",
        back_populates="evaluacion",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Evaluacion(id={self.evaluar_id}, calidad={self.calidad})"