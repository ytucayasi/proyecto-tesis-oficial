# curso_usuario/curso_usuario_entity.py
from src.config import config
from sqlalchemy import Integer, DateTime, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.usuarios.usuarios_entity import Usuarios  # Cambiado para coincidir con tu clase
    from src.cursos.cursos_entity import Curso

class CursoUsuarioEntity(config.Base):
    __tablename__ = "curso_usuario"

    curso_usuario_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    
    curso_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cursos.curso_id", ondelete="CASCADE"),
        nullable=False
    )
    
    usuario_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("usuarios.usuario_id", ondelete="CASCADE"),
        nullable=False
    )
    
    fecha_asignacion: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=date.today
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relaciones
    curso: Mapped["Curso"] = relationship(
        "Curso",
        back_populates="usuarios",
        lazy="select"
    )

    usuario: Mapped["Usuarios"] = relationship(  # Cambiado para coincidir con tu clase
        "Usuarios",
        back_populates="cursos",
        lazy="select"
    )

    def __repr__(self) -> str:
        return f"CursoUsuario(id={self.curso_usuario_id}, curso_id={self.curso_id}, usuario_id={self.usuario_id})"