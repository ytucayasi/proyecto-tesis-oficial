from src.config import config
from sqlalchemy import Integer, String, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime

class Persona(config.Base):
    __tablename__ = "personas"

    persona_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(60), nullable=False)
    apellido_p: Mapped[str] = mapped_column(String(30), nullable=False)
    apellido_m: Mapped[str] = mapped_column(String(30))
    telefono: Mapped[str] = mapped_column(String(15))
    direccion: Mapped[str] = mapped_column(String(255))
    fecha_nacimiento: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)