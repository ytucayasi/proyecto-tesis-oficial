from nest.core import Controller, Post, Depends
from fastapi import UploadFile, File, Form
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .document_processing_service import DocumentProcessingService
from .document_processing_model import DocumentProcessingResponse

@Controller("document-processing")
class DocumentProcessingController:
    def __init__(self, document_processing_service: DocumentProcessingService):
        self.document_processing_service = document_processing_service

    @Post("/process")
    async def process_document(
        self,
        file: UploadFile = File(...),
        topic: Optional[str] = Form(None),
        chunk_size: Optional[int] = Form(1000),
        chunk_overlap: Optional[int] = Form(200),
        session: AsyncSession = Depends(config.get_db)
    ) -> DocumentProcessingResponse:
        return await self.document_processing_service.process_document(
            file=file,
            topic=topic,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            session=session
        )