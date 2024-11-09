from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .sesion_aprendizaje_service import SesionAprendizajeService
from .sesion_aprendizaje_model import SesionAprendizaje, UpdateSesionAprendizaje, SesionAprendizajeResponse
from typing import List

@Controller("sesiones-aprendizaje")
class SesionAprendizajeController:
    def __init__(self, sesion_service: SesionAprendizajeService):
        self.sesion_service = sesion_service

    @Get("/")
    async def get_sesiones(
        self, 
        session: AsyncSession = Depends(config.get_db)
    ) -> List[SesionAprendizajeResponse]:
        return await self.sesion_service.get_sesiones(session)
    
    @Get("/unidad/:unidad_id/")
    async def get_sesiones_by_unidad(
        self,
        unidad_id: int,
        session: AsyncSession = Depends(config.get_db)
    ) -> List[SesionAprendizajeResponse]:
        return await self.sesion_service.get_sesiones_by_unidad(unidad_id, session)
        
    @Get("/:sesion_id/")
    async def get_sesion(
        self, 
        sesion_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ) -> SesionAprendizajeResponse:
        return await self.sesion_service.get_sesion_by_id(
            sesion_id, 
            session
        )
        
    @Post("/")
    async def create_sesion(
        self, 
        sesion: SesionAprendizaje, 
        session: AsyncSession = Depends(config.get_db)
    ) -> SesionAprendizajeResponse:
        return await self.sesion_service.create_sesion(
            sesion, 
            session
        )
        
    @Put("/:sesion_id/")
    async def update_sesion(
        self, 
        sesion_id: int, 
        sesion: UpdateSesionAprendizaje, 
        session: AsyncSession = Depends(config.get_db)
    ) -> SesionAprendizajeResponse:
        return await self.sesion_service.update_sesion(
            sesion_id, 
            sesion, 
            session
        )
        
    @Delete("/:sesion_id/")
    async def delete_sesion(
        self, 
        sesion_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ):
        await self.sesion_service.delete_sesion(sesion_id, session)
        return {"message": "Sesión de aprendizaje eliminada exitosamente"}