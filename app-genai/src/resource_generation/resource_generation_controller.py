from nest.core import Controller, Post, Depends
from fastapi import UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .resource_generation_service import ResourceGenerationService
from .resource_generation_model import ResourceGenerationResponse

@Controller("resource-generation")
class ResourceGenerationController:
    def __init__(self, resource_generation_service: ResourceGenerationService):
        self.resource_generation_service = resource_generation_service

    @Post("/generate")
    async def generate_resource(
        self,
        file: UploadFile = File(...),
        titulo: str = Form(...),
        modelo: str = Form(...),
        diseno: int = Form(...),
        tipo_recurso: str = Form(...),
        cantidad_paginas: int = Form(...),
        session: AsyncSession = Depends(config.get_db)
    ) -> ResourceGenerationResponse:
        return await self.resource_generation_service.generate_resource(
            file=file,
            titulo=titulo,
            modelo=modelo,
            diseno=diseno,
            tipo_recurso=tipo_recurso,
            cantidad_paginas=cantidad_paginas,
            session=session
        )