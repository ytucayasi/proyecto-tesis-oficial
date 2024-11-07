from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .unidad_service import UnidadService
from .unidad_model import Unidad, UpdateUnidad, UnidadResponse
from typing import List

@Controller("unidades")  # Quitamos el /api/ del prefijo
class UnidadController:
    def __init__(self, unidad_service: UnidadService):
        self.unidad_service = unidad_service

    @Get("/")  # Cambiado de "" a "/"
    async def get_unidades(
        self, 
        session: AsyncSession = Depends(config.get_db)
    ) -> List[UnidadResponse]:
        return await self.unidad_service.get_unidades(session)
    
    @Get("/curso/:curso_id/")  # Agregado trailing slash
    async def get_unidades_by_curso(
        self,
        curso_id: int,
        session: AsyncSession = Depends(config.get_db)
    ) -> List[UnidadResponse]:
        return await self.unidad_service.get_unidades_by_curso(curso_id, session)
        
    @Get("/:unidad_id/")  # Agregado trailing slash
    async def get_unidad(
        self, 
        unidad_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ) -> UnidadResponse:
        return await self.unidad_service.get_unidad_by_id(
            unidad_id, 
            session
        )
        
    @Post("/")  # Cambiado de "" a "/"
    async def create_unidad(
        self, 
        unidad: Unidad, 
        session: AsyncSession = Depends(config.get_db)
    ) -> UnidadResponse:
        return await self.unidad_service.create_unidad(
            unidad, 
            session
        )
        
    @Put("/:unidad_id/")  # Agregado trailing slash
    async def update_unidad(
        self, 
        unidad_id: int, 
        unidad: UpdateUnidad, 
        session: AsyncSession = Depends(config.get_db)
    ) -> UnidadResponse:
        return await self.unidad_service.update_unidad(
            unidad_id, 
            unidad, 
            session
        )
        
    @Delete("/:unidad_id/")  # Agregado trailing slash
    async def delete_unidad(
        self, 
        unidad_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ):
        await self.unidad_service.delete_unidad(unidad_id, session)
        return {"message": "Unidad eliminada exitosamente"}