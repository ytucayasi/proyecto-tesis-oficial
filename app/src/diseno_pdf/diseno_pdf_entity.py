# diseno_pdf_entity.py
from src.config import config
from sqlalchemy import Integer, String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.generacion_recurso.generacion_recurso_entity import GeneracionRecursoEntity

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

    # Relación con GeneracionRecurso
    generaciones_recurso: Mapped[List["GeneracionRecursoEntity"]] = relationship(
        "GeneracionRecursoEntity",
        back_populates="diseno",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"DisenoPdf(id={self.diseno_pdf_id}, nombre='{self.nombre}')"

# diseno_pdf_model.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .diseno_pdf_entity import EstadoDiseno

class DisenoPdfBase(BaseModel):
    nombre: str
    link_archivo: str
    estado: EstadoDiseno = EstadoDiseno.ACTIVO

class DisenoPdf(DisenoPdfBase):
    pass

class UpdateDisenoPdf(BaseModel):
    nombre: Optional[str] = None
    link_archivo: Optional[str] = None
    estado: Optional[EstadoDiseno] = None

class DisenoPdfResponse(DisenoPdfBase):
    diseno_pdf_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True