from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .tipo_secuencia_service import TipoSecuenciaService
from .tipo_secuencia_model import TipoSecuencia, UpdateTipoSecuencia, TipoSecuenciaResponse
from typing import List

@Controller("tipos-secuencia")
class TipoSecuenciaController:
    def __init__(self, tipo_secuencia_service: TipoSecuenciaService):
        self.tipo_secuencia_service = tipo_secuencia_service

    @Get("/")
    async def get_tipos_secuencia(
        self, 
        session: AsyncSession = Depends(config.get_db)
    ) -> List[TipoSecuenciaResponse]:
        return await self.tipo_secuencia_service.get_tipos_secuencia(session)
        
    @Get("/:tipo_id/")
    async def get_tipo_secuencia(
        self, 
        tipo_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ) -> TipoSecuenciaResponse:
        return await self.tipo_secuencia_service.get_tipo_secuencia_by_id(
            tipo_id, 
            session
        )
        
    @Post("/")
    async def create_tipo_secuencia(
        self, 
        tipo_secuencia: TipoSecuencia, 
        session: AsyncSession = Depends(config.get_db)
    ) -> TipoSecuenciaResponse:
        return await self.tipo_secuencia_service.create_tipo_secuencia(
            tipo_secuencia, 
            session
        )
        
    @Put("/:tipo_id/")
    async def update_tipo_secuencia(
        self, 
        tipo_id: int, 
        tipo_secuencia: UpdateTipoSecuencia, 
        session: AsyncSession = Depends(config.get_db)
    ) -> TipoSecuenciaResponse:
        return await self.tipo_secuencia_service.update_tipo_secuencia(
            tipo_id, 
            tipo_secuencia, 
            session
        )
        
    @Delete("/:tipo_id/")
    async def delete_tipo_secuencia(
        self, 
        tipo_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ):
        await self.tipo_secuencia_service.delete_tipo_secuencia(tipo_id, session)
        return {"message": "Tipo de secuencia eliminado exitosamente"}