from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .ciclos_cursos_service import CiclosCursosService
from .ciclos_cursos_model import CicloCurso, UpdateCicloCurso

@Controller("ciclos_cursos")
class CiclosCursosController:
    def __init__(self, ciclos_cursos_service: CiclosCursosService):
        self.ciclos_cursos_service = ciclos_cursos_service

    @Get("/")
    async def get_ciclos_cursos(self, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_cursos_service.get_ciclos_cursos(session)
        
    @Get("/{ciclo_curso_id}")
    async def get_ciclo_curso(self, ciclo_curso_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_cursos_service.get_ciclo_curso_by_id(ciclo_curso_id, session)
        
    @Post("/")
    async def create_ciclo_curso(self, ciclo_curso: CicloCurso, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_cursos_service.create_ciclo_curso(ciclo_curso, session)
        
    @Put("/{ciclo_curso_id}")
    async def update_ciclo_curso(self, ciclo_curso_id: int, ciclo_curso: UpdateCicloCurso, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_cursos_service.update_ciclo_curso(ciclo_curso_id, ciclo_curso, session)
        
    @Delete("/{ciclo_curso_id}")
    async def delete_ciclo_curso(self, ciclo_curso_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.ciclos_cursos_service.delete_ciclo_curso(ciclo_curso_id, session)
