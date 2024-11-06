from src.config import config
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.niveles.niveles_entity import Nivel
from src.facultades.facultades_entity import Facultad

class EscuelaProfesional(config.Base):
    __tablename__ = "escuelas_profesionales"

    escuela_profesional_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nivel_id: Mapped[int] = mapped_column(ForeignKey("niveles.nivel_id"), nullable=False)
    facultad_id: Mapped[int] = mapped_column(ForeignKey("facultades.facultad_id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    codigo: Mapped[str] = mapped_column(String(15), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text)
    estado: Mapped[int] = mapped_column(SmallInteger, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    nivel: Mapped["Nivel"] = relationship("Nivel", backref="escuelas_profesionales")
    facultad: Mapped["Facultad"] = relationship("Facultad", backref="escuelas_profesionales")
