from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .curso_equivalencias_service import CursoEquivalenciasService
from .curso_equivalencias_model import CursoEquivalencias, UpdateCursoEquivalencias

@Controller("curso_equivalencias")
class CursoEquivalenciasController:

    def __init__(self, curso_equivalencias_service: CursoEquivalenciasService):
        self.curso_equivalencias_service = curso_equivalencias_service

    @Get("/")
    async def get_curso_equivalencias(self, session: AsyncSession = Depends(config.get_db)):
        return await self.curso_equivalencias_service.get_curso_equivalencias(session)

    @Get("/{curso_equivalencia_id}")
    async def get_curso_equivalencia_by_id(self, curso_equivalencia_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.curso_equivalencias_service.get_curso_equivalencia_by_id(curso_equivalencia_id, session)

    @Post("/")
    async def add_curso_equivalencia(self, curso_equivalencia: CursoEquivalencias, session: AsyncSession = Depends(config.get_db)):
        return await self.curso_equivalencias_service.add_curso_equivalencia(curso_equivalencia, session)

    @Put("/{curso_equivalencia_id}")
    async def update_curso_equivalencia(self, curso_equivalencia_id: int, curso_equivalencia_update: UpdateCursoEquivalencias, session: AsyncSession = Depends(config.get_db)):
        return await self.curso_equivalencias_service.update_curso_equivalencia(curso_equivalencia_id, curso_equivalencia_update, session)

    @Delete("/{curso_equivalencia_id}")
    async def delete_curso_equivalencia(self, curso_equivalencia_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.curso_equivalencias_service.delete_curso_equivalencia(curso_equivalencia_id, session)
