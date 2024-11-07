from src.config import config
from sqlalchemy import Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.generacion_recurso.generacion_recurso_entity import GeneracionRecursoEntity
    from src.evaluaciones.evaluaciones_entity import Evaluaciones

class EstadoRecurso(str, enum.Enum):
    ACTIVO = 'activo'
    INACTIVO = 'inactivo'

class HistorialRecursoEntity(config.Base):
    __tablename__ = "historial_recurso"

    historial_recurso_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    
    generacion_recurso_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("generacion_recurso.generacion_recurso_id", ondelete="CASCADE"),
        nullable=False
    )
    
    evaluacion_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("evaluaciones.evaluar_id", ondelete="CASCADE"),  # Corregido el nombre de la tabla
        nullable=False
    )
    
    fecha_generacion: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    
    estado_recurso: Mapped[EstadoRecurso] = mapped_column(
        Enum(EstadoRecurso, name='estado_recurso', create_type=False),
        nullable=False,
        default=EstadoRecurso.ACTIVO
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relaciones
    generacion_recurso: Mapped["GeneracionRecursoEntity"] = relationship(
        "GeneracionRecursoEntity",
        back_populates="historiales",
        lazy="select"
    )

    evaluacion: Mapped["Evaluaciones"] = relationship(
        "Evaluaciones",
        back_populates="historiales",
        lazy="select"
    )

    def __repr__(self) -> str:
        return f"HistorialRecurso(id={self.historial_recurso_id}, estado={self.estado_recurso})"