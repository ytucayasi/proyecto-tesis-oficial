from src.config import config
from sqlalchemy import Integer, ForeignKey, String, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class CursoEquivalencias(config.Base):
    __tablename__ = "curso_equivalencias"

    curso_equivalencia_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    curso_id: Mapped[int] = mapped_column(Integer)
    curso_equivalencia_id_fk: Mapped[int] = mapped_column(Integer)
    tipo_equivalencia: Mapped[str] = mapped_column(String(50))
    fecha_equivalencia: Mapped[datetime] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
