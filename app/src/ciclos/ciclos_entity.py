from src.config import config
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.programas.programas_entity import Programa

class Ciclo(config.Base):
    __tablename__ = "ciclos"

    ciclo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    programa_id: Mapped[int] = mapped_column(ForeignKey("programas.programa_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    numero_ciclo: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[int] = mapped_column(SmallInteger, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación
    programa: Mapped["Programa"] = relationship("Programa", backref="ciclos")
