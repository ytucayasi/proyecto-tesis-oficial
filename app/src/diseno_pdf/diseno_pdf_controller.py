from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .diseno_pdf_service import DisenoPdfService
from .diseno_pdf_model import DisenoPdf, UpdateDisenoPdf, DisenoPdfResponse
from typing import List

@Controller("diseno-pdf")
class DisenoPdfController:
    def __init__(self, diseno_pdf_service: DisenoPdfService):
        self.diseno_pdf_service = diseno_pdf_service

    @Get("/")
    async def get_diseno_pdfs(
        self, 
        session: AsyncSession = Depends(config.get_db)
    ) -> List[DisenoPdfResponse]:
        return await self.diseno_pdf_service.get_diseno_pdfs(session)
        
    @Get("/{diseno_pdf_id}")
    async def get_diseno_pdf(
        self, 
        diseno_pdf_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ) -> DisenoPdfResponse:
        return await self.diseno_pdf_service.get_diseno_pdf_by_id(
            diseno_pdf_id, 
            session
        )
        
    @Post("/")
    async def create_diseno_pdf(
        self, 
        diseno_pdf: DisenoPdf, 
        session: AsyncSession = Depends(config.get_db)
    ) -> DisenoPdfResponse:
        return await self.diseno_pdf_service.create_diseno_pdf(
            diseno_pdf, 
            session
        )
        
    @Put("/{diseno_pdf_id}")
    async def update_diseno_pdf(
        self, 
        diseno_pdf_id: int, 
        diseno_pdf: UpdateDisenoPdf, 
        session: AsyncSession = Depends(config.get_db)
    ) -> DisenoPdfResponse:
        return await self.diseno_pdf_service.update_diseno_pdf(
            diseno_pdf_id, 
            diseno_pdf, 
            session
        )
        
    @Delete("/{diseno_pdf_id}")
    async def delete_diseno_pdf(
        self, 
        diseno_pdf_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ):
        await self.diseno_pdf_service.delete_diseno_pdf(diseno_pdf_id, session)
        return {"message": "Diseño PDF eliminado exitosamente"}