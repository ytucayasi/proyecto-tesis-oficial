from pydantic import BaseModel
from typing import Optional

class Privilegios(BaseModel):
    nombre_privilegio: str
    descripcion: str

class UpdatePrivilegios(BaseModel):
    nombre_privilegio: Optional[str] = None
    descripcion: Optional[str] = None
