from src.config import config
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.generacion_recurso.generacion_recurso_entity import GeneracionRecursoEntity

class InputEntity(config.Base):
    __tablename__ = "input"

    input_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
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

    # Relación con GeneracionRecurso
    generaciones_recurso: Mapped[List["GeneracionRecursoEntity"]] = relationship(
        "GeneracionRecursoEntity",
        back_populates="input",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"Input(input_id={self.input_id})"