from src.config import config
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Sesiones(config.Base):
    __tablename__ = "sesiones"

    sesion_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(Integer)
    token: Mapped[str] = mapped_column(String(512))
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_expiracion: Mapped[datetime] = mapped_column(DateTime)
    estado: Mapped[bool] = mapped_column(Boolean, default=True)
