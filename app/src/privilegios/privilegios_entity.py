from src.config import config
from sqlalchemy import Integer, String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Privilegios(config.Base):
    __tablename__ = "privilegios"

    privilegio_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_privilegio: Mapped[str] = mapped_column(String(50), unique=True)
    descripcion: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
