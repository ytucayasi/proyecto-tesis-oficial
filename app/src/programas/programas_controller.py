from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .programas_service import ProgramasService
from .programas_model import Programa, UpdatePrograma

@Controller("programas")
class ProgramasController:
    def __init__(self, programas_service: ProgramasService):
        self.programas_service = programas_service

    @Get("/")
    async def get_programas(self, session: AsyncSession = Depends(config.get_db)):
        return await self.programas_service.get_programas(session)

    @Get("/{programa_id}")
    async def get_programa(self, programa_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.programas_service.get_programa_by_id(programa_id, session)

    @Post("/")
    async def create_programa(self, programa: Programa, session: AsyncSession = Depends(config.get_db)):
        return await self.programas_service.create_programa(programa, session)

    @Put("/{programa_id}")
    async def update_programa(self, programa_id: int, programa: UpdatePrograma, session: AsyncSession = Depends(config.get_db)):
        return await self.programas_service.update_programa(programa_id, programa, session)

    @Delete("/{programa_id}")
    async def delete_programa(self, programa_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.programas_service.delete_programa(programa_id, session)
