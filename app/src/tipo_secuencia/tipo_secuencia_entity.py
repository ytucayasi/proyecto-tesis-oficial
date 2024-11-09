from src.config import config
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class TipoSecuenciaEntity(config.Base):
    __tablename__ = "tipo_secuencia"

    tipo_secuencia_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    
    nombre: Mapped[str] = mapped_column(
        String(255), 
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

    def __repr__(self) -> str:
        return f"TipoSecuencia(id={self.tipo_secuencia_id}, nombre='{self.nombre}')"