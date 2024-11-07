from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .sesiones_service import SesionesService
from .sesiones_model import Sesiones, UpdateSesiones

@Controller("sesiones")
class SesionesController:

    def __init__(self, sesiones_service: SesionesService):
        self.sesiones_service = sesiones_service

    @Get("/")
    async def get_sesiones(self, session: AsyncSession = Depends(config.get_db)):
        return await self.sesiones_service.get_sesiones(session)

    @Get("/{sesion_id}")
    async def get_sesion_by_id(self, sesion_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.sesiones_service.get_sesion_by_id(sesion_id, session)

    @Post("/")
    async def add_sesion(self, sesion: Sesiones, session: AsyncSession = Depends(config.get_db)):
        return await self.sesiones_service.add_sesion(sesion, session)

    @Put("/{sesion_id}")
    async def update_sesion(self, sesion_id: int, sesion_update: UpdateSesiones, session: AsyncSession = Depends(config.get_db)):
        return await self.sesiones_service.update_sesion(sesion_id, sesion_update, session)

    @Delete("/{sesion_id}")
    async def delete_sesion(self, sesion_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.sesiones_service.delete_sesion(sesion_id, session)
