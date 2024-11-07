from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .ciclos_service import CiclosService
from .ciclos_model import Ciclo, UpdateCiclo

@Controller("ciclos")
class CiclosController:
    def __init__(self, ciclos_service: CiclosService):
        self.ciclos_service = ciclos_service

    @Get("/")
    async def get_ciclos(self, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_service.get_ciclos(session)

    @Get("/{ciclo_id}")
    async def get_ciclo(self, ciclo_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_service.get_ciclo_by_id(ciclo_id, session)

    @Post("/")
    async def create_ciclo(self, ciclo: Ciclo, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_service.create_ciclo(ciclo, session)

    @Put("/{ciclo_id}")
    async def update_ciclo(self, ciclo_id: int, ciclo: UpdateCiclo, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_service.update_ciclo(ciclo_id, ciclo, session)

    @Delete("/{ciclo_id}")
    async def delete_ciclo(self, ciclo_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_service.delete_ciclo(ciclo_id, session)
