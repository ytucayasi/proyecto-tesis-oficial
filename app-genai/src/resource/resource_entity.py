from src.config import config
from sqlalchemy import Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum

class TipoRecurso(str, enum.Enum):
    WORD = 'word'
    PPT = 'ppt'
    PDF = 'pdf'

class ResourceEntity(config.Base):
    __tablename__ = "resources"

    resource_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    input_url: Mapped[str] = mapped_column(String(255), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)
    diseno: Mapped[int] = mapped_column(Integer, nullable=False)
    cantidad_paginas: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_recurso: Mapped[TipoRecurso] = mapped_column(Enum(TipoRecurso), nullable=False)
    url_recurso: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)