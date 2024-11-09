from src.config import config
from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class UsuarioRoles(config.Base):
    __tablename__ = "usuario_roles"

    usuario_rol_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer)
    rol_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
