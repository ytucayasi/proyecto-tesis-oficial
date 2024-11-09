from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .secuencia_aprendizaje_service import SecuenciaAprendizajeService
from .secuencia_aprendizaje_model import (
    SecuenciaAprendizaje,
    UpdateSecuenciaAprendizaje,
    SecuenciaAprendizajeResponse
)
from typing import List

@Controller("secuencias-aprendizaje")
class SecuenciaAprendizajeController:
    def __init__(self, secuencia_service: SecuenciaAprendizajeService):
        self.secuencia_service = secuencia_service

    @Get("/")
    async def get_secuencias(
        self, 
        session: AsyncSession = Depends(config.get_db)
    ) -> List[SecuenciaAprendizajeResponse]:
        return await self.secuencia_service.get_secuencias(session)
    
    @Get("/sesion/:sesion_id/")
    async def get_secuencias_by_sesion(
        self,
        sesion_id: int,
        session: AsyncSession = Depends(config.get_db)
    ) -> List[SecuenciaAprendizajeResponse]:
        return await self.secuencia_service.get_secuencias_by_sesion(sesion_id, session)
        
    @Get("/:secuencia_id/")
    async def get_secuencia(
        self, 
        secuencia_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ) -> SecuenciaAprendizajeResponse:
        return await self.secuencia_service.get_secuencia_by_id(
            secuencia_id, 
            session
        )
        
    @Post("/")
    async def create_secuencia(
        self, 
        secuencia: SecuenciaAprendizaje, 
        session: AsyncSession = Depends(config.get_db)
    ) -> SecuenciaAprendizajeResponse:
        return await self.secuencia_service.create_secuencia(
            secuencia, 
            session
        )
        
    @Put("/:secuencia_id/")
    async def update_secuencia(
        self, 
        secuencia_id: int, 
        secuencia: UpdateSecuenciaAprendizaje, 
        session: AsyncSession = Depends(config.get_db)
    ) -> SecuenciaAprendizajeResponse:
        return await self.secuencia_service.update_secuencia(
            secuencia_id, 
            secuencia, 
            session
        )
        
    @Delete("/:secuencia_id/")
    async def delete_secuencia(
        self, 
        secuencia_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ):
        await self.secuencia_service.delete_secuencia(secuencia_id, session)
        return {"message": "Secuencia de aprendizaje eliminada exitosamente"}