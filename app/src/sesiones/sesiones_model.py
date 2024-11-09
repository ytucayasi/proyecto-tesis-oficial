from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Sesiones(BaseModel):
    usuario_id: int
    token: str
    fecha_expiracion: datetime
    estado: Optional[bool] = True

class UpdateSesiones(BaseModel):
    token: Optional[str] = None
    fecha_expiracion: Optional[datetime] = None
    estado: Optional[bool] = None
