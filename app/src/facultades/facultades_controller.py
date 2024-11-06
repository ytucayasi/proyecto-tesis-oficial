from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .facultades_service import FacultadesService
from .facultades_model import Facultad, UpdateFacultad

@Controller("facultades")
class FacultadesController:
    def __init__(self, facultades_service: FacultadesService):
        self.facultades_service = facultades_service

    @Get("/")
    async def get_facultades(self, session: AsyncSession = Depends(config.get_db)):
        return await self.facultades_service.get_facultades(session)
        
    @Get("/{facultad_id}")
    async def get_facultad(self, facultad_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.facultades_service.get_facultad_by_id(facultad_id, session)
        
    @Post("/")
    async def create_facultad(self, facultad: Facultad, session: AsyncSession = Depends(config.get_db)):
        return await self.facultades_service.create_facultad(facultad, session)
        
    @Put("/{facultad_id}")
    async def update_facultad(self, facultad_id: int, facultad: UpdateFacultad, session: AsyncSession = Depends(config.get_db)):
        return await self.facultades_service.update_facultad(facultad_id, facultad, session)
        
    @Delete("/{facultad_id}")
    async def delete_facultad(self, facultad_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.facultades_service.delete_facultad(facultad_id, session)