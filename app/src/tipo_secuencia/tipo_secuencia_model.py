from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TipoSecuenciaBase(BaseModel):
    nombre: str
    descripcion: str

class TipoSecuencia(TipoSecuenciaBase):
    pass

class UpdateTipoSecuencia(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class TipoSecuenciaResponse(TipoSecuenciaBase):
    tipo_secuencia_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True