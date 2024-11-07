from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .evaluaciones_service import EvaluacionesService
from .evaluaciones_model import Evaluaciones, UpdateEvaluaciones

@Controller("evaluaciones")
class EvaluacionesController:

    def __init__(self, evaluaciones_service: EvaluacionesService):
        self.evaluaciones_service = evaluaciones_service

    @Get("/")
    async def get_evaluaciones(self, session: AsyncSession = Depends(config.get_db)):
        return await self.evaluaciones_service.get_evaluaciones(session)

    @Get("/{evaluar_id}")
    async def get_evaluacion_by_id(self, evaluar_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.evaluaciones_service.get_evaluacion_by_id(evaluar_id, session)

    @Post("/")
    async def add_evaluacion(self, evaluacion: Evaluaciones, session: AsyncSession = Depends(config.get_db)):
        return await self.evaluaciones_service.add_evaluacion(evaluacion, session)

    @Put("/{evaluar_id}")
    async def update_evaluacion(self, evaluar_id: int, evaluacion_update: UpdateEvaluaciones, session: AsyncSession = Depends(config.get_db)):
        return await self.evaluaciones_service.update_evaluacion(evaluar_id, evaluacion_update, session)

    @Delete("/{evaluar_id}")
    async def delete_evaluacion(self, evaluar_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.evaluaciones_service.delete_evaluacion(evaluar_id, session)
