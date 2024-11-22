from nest.core import Controller, Post, Get, Depends
from fastapi import UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .resource_generation_service import ResourceGenerationService
from .resource_generation_model import ResourceGenerationResponse

@Controller("resource-generation")
class ResourceGenerationController:
    def __init__(self, resource_generation_service: ResourceGenerationService):
        self.resource_generation_service = resource_generation_service

    @Get("/files/{filename}")
    async def get_file(self, filename: str):
        # Handle PDF files in subdirectory
        if filename.endswith('.pdf'):
            file_path = Path("generated_resources/pdf") / filename
        else:
            file_path = Path("generated_resources") / filename
            
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
            
        # Set media type based on file extension
        media_type = 'application/pdf' if filename.endswith('.pdf') else \
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type=media_type
        )

    @Get("/view/{filename}")
    async def view_file(self, filename: str):
        if filename.endswith('.pdf'):
            file_path = Path("generated_resources/pdf") / filename 
        else:
            file_path = Path("generated_resources") / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
            
        media_type = 'application/pdf' if filename.endswith('.pdf') else \
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                        
        return FileResponse(
            path=file_path,
            media_type=media_type
        )

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