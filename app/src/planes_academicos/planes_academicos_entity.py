from src.config import config
from sqlalchemy import Integer, String, Text, DateTime, Date, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.escuelas_profesionales.escuelas_profesionales_entity import EscuelaProfesional

class PlanAcademico(config.Base):
    __tablename__ = "planes_academicos"

    plan_academico_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    escuela_profesional_id: Mapped[int] = mapped_column(ForeignKey("escuelas_profesionales.escuela_profesional_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    anio_inicio: Mapped[datetime] = mapped_column(Date, nullable=False)
    anio_fin: Mapped[datetime] = mapped_column(Date, nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    estado: Mapped[int] = mapped_column(SmallInteger, default=1)
    creditos_totales: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación
    escuela_profesional: Mapped["EscuelaProfesional"] = relationship("EscuelaProfesional", backref="planes_academicos")
