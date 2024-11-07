from src.config import config
from sqlalchemy import Integer, ForeignKey, Enum, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from enum import Enum as PyEnum

class TipoReplicacionEnum(PyEnum):
    curso = "curso"
    plan = "plan"

class EquivalenciaReplicadas(config.Base):
    __tablename__ = "equivalencia_replicadas"

    equivalencia_replicada_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curso_id: Mapped[int] = mapped_column(Integer, nullable=True)
    plan_academico_id: Mapped[int] = mapped_column(Integer, nullable=True)
    tipo_replicacion: Mapped[TipoReplicacionEnum] = mapped_column(Enum(TipoReplicacionEnum))
    fecha_replicacion: Mapped[datetime] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
