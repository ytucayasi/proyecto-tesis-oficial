# generacion_recurso_entity.py
from src.config import config
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.input.input_entity import InputEntity
    from src.diseno_pdf.diseno_pdf_entity import DisenoPdfEntity
    from src.secuencia_aprendizaje.secuencia_aprendizaje_entity import SecuenciaAprendizajeEntity
    from src.historial_recurso.historial_recurso_entity import HistorialRecursoEntity

class TipoDocumento(str, enum.Enum):
    WORD = 'word'
    PDF = 'pdf'
    PPT = 'ppt'

class GeneracionRecursoEntity(config.Base):
    __tablename__ = "generacion_recurso"

    generacion_recurso_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    
    input_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("input.input_id", ondelete="CASCADE"),
        nullable=False
    )
    
    diseno_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("diseno_pdf.diseno_pdf_id", ondelete="CASCADE"),
        nullable=False
    )
    
    secuencia_aprendizaje_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("secuencia_aprendizaje.secuencia_aprendizaje_id", ondelete="CASCADE"),
        nullable=False
    )
    
    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.usuario_id", ondelete="CASCADE"),
        nullable=False
    )
    
    numero_paginas: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    tipo_documento: Mapped[TipoDocumento] = mapped_column(
        Enum(TipoDocumento, name='tipodocumento', create_type=False),
        nullable=False
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

    # Relaciones existentes
    input: Mapped["InputEntity"] = relationship(
        "InputEntity",
        back_populates="generaciones_recurso",
        lazy="select"
    )

    diseno: Mapped["DisenoPdfEntity"] = relationship(
        "DisenoPdfEntity",
        back_populates="generaciones_recurso",
        lazy="select"
    )

    secuencia_aprendizaje: Mapped["SecuenciaAprendizajeEntity"] = relationship(
        "SecuenciaAprendizajeEntity",
        back_populates="generaciones_recurso",
        lazy="select"
    )

    # Nueva relación con HistorialRecurso
    historiales: Mapped[List["HistorialRecursoEntity"]] = relationship(
        "HistorialRecursoEntity",
        back_populates="generacion_recurso",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"GeneracionRecurso(id={self.generacion_recurso_id}, tipo={self.tipo_documento})"