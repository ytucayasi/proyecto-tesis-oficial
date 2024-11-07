from src.config import config
from sqlalchemy import Integer, ForeignKey, Text, Date, Enum, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum

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
