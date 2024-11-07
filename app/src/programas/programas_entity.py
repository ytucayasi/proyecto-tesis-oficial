from src.config import config
from sqlalchemy import Integer, String, Text, DateTime, Date, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.planes_academicos.planes_academicos_entity import PlanAcademico

class Programa(config.Base):
    __tablename__ = "programas"

    programa_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plan_academico_id: Mapped[int] = mapped_column(ForeignKey("planes_academicos.plan_academico_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    estado: Mapped[int] = mapped_column(SmallInteger, default=1)
    fecha_inicio: Mapped[datetime] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[datetime] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación
    plan_academico: Mapped["PlanAcademico"] = relationship("PlanAcademico", backref="programas")
