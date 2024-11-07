from pydantic import BaseModel
from typing import Optional

class RolPrivilegios(BaseModel):
    rol_id: int
    privilegio_id: int

class UpdateRolPrivilegios(BaseModel):
    rol_id: Optional[int] = None
    privilegio_id: Optional[int] = None
