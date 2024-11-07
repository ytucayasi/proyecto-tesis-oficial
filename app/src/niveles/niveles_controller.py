from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .niveles_service import NivelesService
from .niveles_model import Nivel, UpdateNivel

@Controller("niveles")
class NivelesController:
    def __init__(self, niveles_service: NivelesService):
        self.niveles_service = niveles_service

    @Get("/")
    async def get_niveles(self, session: AsyncSession = Depends(config.get_db)):
        return await self.niveles_service.get_niveles(session)
        
    @Get("/{nivel_id}")
    async def get_nivel(self, nivel_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.niveles_service.get_nivel_by_id(nivel_id, session)
        
    @Post("/")
    async def create_nivel(self, nivel: Nivel, session: AsyncSession = Depends(config.get_db)):
        return await self.niveles_service.create_nivel(nivel, session)
        
    @Put("/{nivel_id}")
    async def update_nivel(self, nivel_id: int, nivel: UpdateNivel, session: AsyncSession = Depends(config.get_db)):
        return await self.niveles_service.update_nivel(nivel_id, nivel, session)
        
    @Delete("/{nivel_id}")
    async def delete_nivel(self, nivel_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.niveles_service.delete_nivel(nivel_id, session)
