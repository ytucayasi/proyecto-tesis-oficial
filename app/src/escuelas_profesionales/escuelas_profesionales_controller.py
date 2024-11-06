from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .escuelas_profesionales_service import EscuelasProfesionalesService
from .escuelas_profesionales_model import EscuelaProfesional, UpdateEscuelaProfesional

@Controller("escuelas_profesionales")
class EscuelasProfesionalesController:
    def __init__(self, escuelas_profesionales_service: EscuelasProfesionalesService):
        self.escuelas_profesionales_service = escuelas_profesionales_service

    @Get("/")
    async def get_escuelas_profesionales(self, session: AsyncSession = Depends(config.get_db)):
        return await self.escuelas_profesionales_service.get_escuelas_profesionales(session)
        
    @Get("/{escuela_profesional_id}")
    async def get_escuela_profesional(self, escuela_profesional_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.escuelas_profesionales_service.get_escuela_profesional_by_id(escuela_profesional_id, session)
        
    @Post("/")
    async def create_escuela_profesional(self, escuela_profesional: EscuelaProfesional, session: AsyncSession = Depends(config.get_db)):
        return await self.escuelas_profesionales_service.create_escuela_profesional(escuela_profesional, session)
        
    @Put("/{escuela_profesional_id}")
    async def update_escuela_profesional(self, escuela_profesional_id: int, escuela_profesional: UpdateEscuelaProfesional, session: AsyncSession = Depends(config.get_db)):
        return await self.escuelas_profesionales_service.update_escuela_profesional(escuela_profesional_id, escuela_profesional, session)
        
    @Delete("/{escuela_profesional_id}")
    async def delete_escuela_profesional(self, escuela_profesional_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.escuelas_profesionales_service.delete_escuela_profesional(escuela_profesional_id, session)
