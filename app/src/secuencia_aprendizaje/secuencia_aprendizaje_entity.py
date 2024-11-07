# secuencia_aprendizaje_entity.py
from src.config import config
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.sesion_aprendizaje.sesion_aprendizaje_entity import SesionAprendizajeEntity
    from src.tipo_secuencia.tipo_secuencia_entity import TipoSecuenciaEntity

class EstadoRecursos(str, enum.Enum):
    COMPLETO = 'completo'
    PARCIAL = 'parcial'
    NINGUNO = 'ninguno'

class SecuenciaAprendizajeEntity(config.Base):
    __tablename__ = "secuencia_aprendizaje"

    secuencia_aprendizaje_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    
    sesion_aprendizaje_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sesion_aprendizaje.sesion_aprendizaje_id", ondelete="CASCADE"),
        nullable=False
    )
    
    tipo_secuencia_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tipo_secuencia.tipo_secuencia_id", ondelete="CASCADE"),
        nullable=False
    )
    
    link_recurso: Mapped[str] = mapped_column(
        String(500), 
        nullable=True
    )
    
    link_rubrica: Mapped[str] = mapped_column(
        String(500), 
        nullable=True
    )
    
    estado_recursos: Mapped[EstadoRecursos] = mapped_column(
        Enum(EstadoRecursos),
        nullable=False,
        default=EstadoRecursos.NINGUNO
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
    sesion_aprendizaje: Mapped["SesionAprendizajeEntity"] = relationship(
        "SesionAprendizajeEntity",
        back_populates="secuencias_aprendizaje",  # Nombre corregido aquí
        lazy="select"
    )

    tipo_secuencia: Mapped["TipoSecuenciaEntity"] = relationship(
        "TipoSecuenciaEntity",
        lazy="select"
    )

    def __repr__(self) -> str:
        return f"SecuenciaAprendizaje(id={self.secuencia_aprendizaje_id})"