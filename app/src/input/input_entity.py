# input_entity.py
from src.config import config
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

class InputEntity(config.Base):
    __tablename__ = "input"

    input_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    
    nombre: Mapped[str] = mapped_column(
        String(255), 
        nullable=False
    )
    
    link_archivo: Mapped[str] = mapped_column(
        String(255), 
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

    # Relación usando strings para evitar referencias circulares
    #generacion_recursos = relationship(
    #    "GeneracionRecursoEntity", 
    #    back_populates="input",
    #    lazy="select",
    #    cascade="all, delete-orphan"
    #)

    #def __repr__(self) -> str:
    #    return f"Input(input_id={self.input_id}, nombre='{self.nombre}')"