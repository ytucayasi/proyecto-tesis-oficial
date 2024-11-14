# generacion_recurso_controller.py
from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Body
from src.config import config
from .generacion_recurso_service import GeneracionRecursoService
from .generacion_recurso_model import (
    GeneracionRecurso,
    UpdateGeneracionRecurso,
    GeneracionRecursoResponse,
    TipoDocumento
)
from typing import List

@Controller("generacion-recursos")
class GeneracionRecursoController:
    def __init__(self, generacion_service: GeneracionRecursoService):
        self.generacion_service = generacion_service

    @Get("/")
    async def get_generaciones(
        self, 
        session: AsyncSession = Depends(config.get_db)
    ) -> List[GeneracionRecursoResponse]:
        return await self.generacion_service.get_generaciones(session)
        
    @Get("/{generacion_id}")
    async def get_generacion(
        self, 
        generacion_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ) -> GeneracionRecursoResponse:
        return await self.generacion_service.get_by_id(
            generacion_id, 
            session
        )
        
    @Post("/")
    async def create_generacion(
        self, 
        generacion: GeneracionRecurso = Body(...), 
        session: AsyncSession = Depends(config.get_db)
    ) -> GeneracionRecursoResponse:
        try:
            return await self.generacion_service.create_generacion(
                generacion, 
                session
            )
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @Put("/{generacion_id}")
    async def update_generacion(
        self, 
        generacion_id: int, 
        generacion: UpdateGeneracionRecurso = Body(...), 
        session: AsyncSession = Depends(config.get_db)
    ) -> GeneracionRecursoResponse:
        try:
            return await self.generacion_service.update_generacion(
                generacion_id, 
                generacion, 
                session
            )
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @Delete("/{generacion_id}")
    async def delete_generacion(
        self, 
        generacion_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ):
        await self.generacion_service.delete_generacion(generacion_id, session)
        return {"message": "Generación de recurso eliminada exitosamente"}