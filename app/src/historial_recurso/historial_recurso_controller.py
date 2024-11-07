from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .historial_recurso_service import HistorialRecursoService
from .historial_recurso_model import (
    HistorialRecurso,
    UpdateHistorialRecurso,
    HistorialRecursoResponse
)
from typing import List

@Controller("historial-recursos")
class HistorialRecursoController:
    def __init__(self, historial_service: HistorialRecursoService):
        self.historial_service = historial_service

    @Get("/")
    async def get_historiales(
        self, 
        session: AsyncSession = Depends(config.get_db)
    ) -> List[HistorialRecursoResponse]:
        return await self.historial_service.get_historiales(session)
    
    @Get("/generacion/:generacion_id/")
    async def get_by_generacion(
        self,
        generacion_id: int,
        session: AsyncSession = Depends(config.get_db)
    ) -> List[HistorialRecursoResponse]:
        return await self.historial_service.get_by_generacion(generacion_id, session)

    @Get("/evaluacion/:evaluacion_id/")
    async def get_by_evaluacion(
        self,
        evaluacion_id: int,
        session: AsyncSession = Depends(config.get_db)
    ) -> List[HistorialRecursoResponse]:
        return await self.historial_service.get_by_evaluacion(evaluacion_id, session)
        
    @Get("/:historial_id/")
    async def get_historial(
        self, 
        historial_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ) -> HistorialRecursoResponse:
        return await self.historial_service.get_by_id(
            historial_id, 
            session
        )
        
    @Post("/")
    async def create_historial(
        self, 
        historial: HistorialRecurso, 
        session: AsyncSession = Depends(config.get_db)
    ) -> HistorialRecursoResponse:
        return await self.historial_service.create_historial(
            historial, 
            session
        )
        
    @Put("/:historial_id/")
    async def update_historial(
        self, 
        historial_id: int, 
        historial: UpdateHistorialRecurso, 
        session: AsyncSession = Depends(config.get_db)
    ) -> HistorialRecursoResponse:
        return await self.historial_service.update_historial(
            historial_id, 
            historial, 
            session
        )
        
    @Delete("/:historial_id/")
    async def delete_historial(
        self, 
        historial_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ):
        await self.historial_service.delete_historial(historial_id, session)
        return {"message": "Historial de recurso eliminado exitosamente"}