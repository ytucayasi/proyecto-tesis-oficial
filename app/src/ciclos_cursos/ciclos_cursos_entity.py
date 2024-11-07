from src.config import config
from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from src.ciclos.ciclos_entity import Ciclo
from src.cursos.cursos_entity import Curso

class CicloCurso(config.Base):
    __tablename__ = "ciclos_cursos"

    ciclo_curso_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ciclo_id: Mapped[int] = mapped_column(ForeignKey("ciclos.ciclo_id"), nullable=False)
    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.curso_id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    ciclo: Mapped["Ciclo"] = relationship("Ciclo", backref="ciclos_cursos")
    curso: Mapped["Curso"] = relationship("Curso", backref="ciclos_cursos")
