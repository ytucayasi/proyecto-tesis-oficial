from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional

class CursoUsuarioBase(BaseModel):
    curso_id: int
    usuario_id: int
    fecha_asignacion: Optional[date] = None

class CursoUsuario(CursoUsuarioBase):
    pass

class UpdateCursoUsuario(BaseModel):
    fecha_asignacion: Optional[date] = None

class CursoUsuarioResponse(CursoUsuarioBase):
    curso_usuario_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True