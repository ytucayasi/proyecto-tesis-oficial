from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .cursos_service import CursosService
from .cursos_model import Curso, UpdateCurso

@Controller("cursos")
class CursosController:
    def __init__(self, cursos_service: CursosService):
        self.cursos_service = cursos_service

    @Get("/")
    async def get_cursos(self, session: AsyncSession = Depends(config.get_db)):
        return await self.cursos_service.get_cursos(session)

    @Get("/{curso_id}")
    async def get_curso(self, curso_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.cursos_service.get_curso_by_id(curso_id, session)

    @Post("/")
    async def create_curso(self, curso: Curso, session: AsyncSession = Depends(config.get_db)):
        return await self.cursos_service.create_curso(curso, session)

    @Put("/{curso_id}")
    async def update_curso(self, curso_id: int, curso: UpdateCurso, session: AsyncSession = Depends(config.get_db)):
        return await self.cursos_service.update_curso(curso_id, curso, session)

    @Delete("/{curso_id}")
    async def delete_curso(self, curso_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.cursos_service.delete_curso(curso_id, session)
