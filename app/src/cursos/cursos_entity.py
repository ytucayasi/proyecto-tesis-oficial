# cursos_entity.py
from src.config import config
from sqlalchemy import Integer, String, Text, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.unidad.unidad_entity import UnidadEntity
    from src.curso_usuario.curso_usuario_entity import CursoUsuarioEntity

class EstadoRecursosEnum(str, enum.Enum):
    completo = "completo"
    parcial = "parcial"
    ninguno = "ninguno"

class EstadoEvaluacionEnum(str, enum.Enum):
    pendiente = "pendiente"
    evaluado = "evaluado"
    asignacion_p = "asignacion_p"
    regeneracion_p = "regeneracion_p"

class Curso(config.Base):
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

    # Relaciones
    unidades: Mapped[List["UnidadEntity"]] = relationship(
        "UnidadEntity",
        back_populates="curso",
        cascade="all, delete-orphan"
    )

    usuarios: Mapped[List["CursoUsuarioEntity"]] = relationship(
        "CursoUsuarioEntity",
        back_populates="curso",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Curso(id={self.curso_id}, nombre='{self.nombre}')"