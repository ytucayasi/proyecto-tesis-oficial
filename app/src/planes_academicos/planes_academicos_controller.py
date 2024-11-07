from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .planes_academicos_service import PlanesAcademicosService
from .planes_academicos_model import PlanAcademico, UpdatePlanAcademico

@Controller("planes_academicos")
class PlanesAcademicosController:
    def __init__(self, planes_academicos_service: PlanesAcademicosService):
        self.planes_academicos_service = planes_academicos_service

    @Get("/")
    async def get_planes_academicos(self, session: AsyncSession = Depends(config.get_db)):
        return await self.planes_academicos_service.get_planes_academicos(session)

    @Get("/{plan_academico_id}")
    async def get_plan_academico(self, plan_academico_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.planes_academicos_service.get_plan_academico_by_id(plan_academico_id, session)

    @Post("/")
    async def create_plan_academico(self, plan_academico: PlanAcademico, session: AsyncSession = Depends(config.get_db)):
        return await self.planes_academicos_service.create_plan_academico(plan_academico, session)

    @Put("/{plan_academico_id}")
    async def update_plan_academico(self, plan_academico_id: int, plan_academico: UpdatePlanAcademico, session: AsyncSession = Depends(config.get_db)):
        return await self.planes_academicos_service.update_plan_academico(plan_academico_id, plan_academico, session)

    @Delete("/{plan_academico_id}")
    async def delete_plan_academico(self, plan_academico_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.planes_academicos_service.delete_plan_academico(plan_academico_id, session)
