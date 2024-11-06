# cursos_entity.py
from src.config import config  # Importar la configuración que tiene el Base
from sqlalchemy import Integer, String, Text, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum

# Definir los posibles estados para los campos ENUM
class EstadoRecursosEnum(str, enum.Enum):
    completo = "completo"
    parcial = "parcial"
    ninguno = "ninguno"

class EstadoEvaluacionEnum(str, enum.Enum):
    pendiente = "pendiente"
    evaluado = "evaluado"
    asignacion_p = "asignacion_p"
    regeneracion_p = "regeneracion_p"

class Curso(config.Base):  # Usar config.Base en lugar de crear uno nuevo
    __tablename__ = "cursos"

    curso_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    estado_recursos: Mapped[EstadoRecursosEnum] = mapped_column(Enum(EstadoRecursosEnum), nullable=False)
    estado_evaluacion: Mapped[EstadoEvaluacionEnum] = mapped_column(Enum(EstadoEvaluacionEnum), nullable=False)
    credito: Mapped[int] = mapped_column(Integer, nullable=False)
    duracion_horas: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)