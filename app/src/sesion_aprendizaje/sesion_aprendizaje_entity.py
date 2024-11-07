# sesion_aprendizaje_entity.py
from src.config import config
from sqlalchemy import Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.unidad.unidad_entity import UnidadEntity
    from src.secuencia_aprendizaje.secuencia_aprendizaje_entity import SecuenciaAprendizajeEntity

class SesionAprendizajeEntity(config.Base):
    __tablename__ = "sesion_aprendizaje"

    sesion_aprendizaje_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    
    unidad_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("unidad.unidad_id", ondelete="CASCADE"),
        nullable=False
    )
    
    tema: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )
    
    fecha_dictado: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    
    numero_sesion: Mapped[int] = mapped_column(
        Integer,
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

    # Relaciones
    unidad: Mapped["UnidadEntity"] = relationship(
        "UnidadEntity",
        back_populates="sesiones_aprendizaje",
        lazy="select"
    )

    secuencias_aprendizaje: Mapped[List["SecuenciaAprendizajeEntity"]] = relationship(
        "SecuenciaAprendizajeEntity",
        back_populates="sesion_aprendizaje",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"SesionAprendizaje(id={self.sesion_aprendizaje_id}, tema='{self.tema}')"