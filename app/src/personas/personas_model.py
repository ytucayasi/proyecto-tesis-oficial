from pydantic import BaseModel
from typing import Optional
from datetime import date

class PersonaBase(BaseModel):
    nombre: str
    apellido_p: str
    apellido_m: str
    telefono: str
    direccion: str
    fecha_nacimiento: date

class Persona(PersonaBase):
    pass

class UpdatePersona(BaseModel):
    nombre: Optional[str] = None
    apellido_p: Optional[str] = None
    apellido_m: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    fecha_nacimiento: Optional[date] = None