# usuarios_entity.py
from src.config import config
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.curso_usuario.curso_usuario_entity import CursoUsuarioEntity

class Usuarios(config.Base):
    __tablename__ = "usuarios"

    usuario_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    persona_id: Mapped[int] = mapped_column(Integer)
    correo_electronico: Mapped[str] = mapped_column(String(100), unique=True)
    contrasena: Mapped[str] = mapped_column(String(255))
    estado: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con CursoUsuario
    cursos: Mapped[List["CursoUsuarioEntity"]] = relationship(
        "CursoUsuarioEntity",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Usuario(id={self.usuario_id}, correo='{self.correo_electronico}')"