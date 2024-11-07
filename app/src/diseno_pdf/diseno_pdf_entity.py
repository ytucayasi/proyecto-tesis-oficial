from src.config import config
from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum

class EstadoDiseno(str, enum.Enum):
    ACTIVO = 'activo'
    INACTIVO = 'inactivo'

class DisenoPdfEntity(config.Base):
    __tablename__ = "diseno_pdf"

    diseno_pdf_id: Mapped[int] = mapped_column(
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
    
    estado: Mapped[EstadoDiseno] = mapped_column(
        Enum(EstadoDiseno),
        nullable=False,
        default=EstadoDiseno.ACTIVO
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

    def __repr__(self) -> str:
        return f"DisenoPdf(id={self.diseno_pdf_id}, nombre='{self.nombre}', estado={self.estado})"