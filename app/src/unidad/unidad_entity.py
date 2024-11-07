from src.config import config
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.sesion_aprendizaje.sesion_aprendizaje_entity import SesionAprendizajeEntity
    from src.cursos.cursos_entity import Curso

class UnidadEntity(config.Base):
    __tablename__ = "unidad"

    unidad_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    
    curso_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cursos.curso_id", ondelete="CASCADE"),
        nullable=False
    )
    
    nombre: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )
    
    resultado_aprendizaje: Mapped[str] = mapped_column(
        Text, 
        nullable=False
    )
    
    descripcion: Mapped[str] = mapped_column(
        Text, 
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
    curso: Mapped["Curso"] = relationship(
        "Curso",
        back_populates="unidades",
        lazy="select"
    )

    sesiones_aprendizaje: Mapped[List["SesionAprendizajeEntity"]] = relationship(
        "SesionAprendizajeEntity",
        back_populates="unidad",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Unidad(unidad_id={self.unidad_id}, nombre='{self.nombre}')"