from nest.core import Controller, Post, Depends
from fastapi import UploadFile, File, Form, HTTPException
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .document_processing_service import DocumentProcessingService
from .document_processing_model import DocumentProcessingResponse, DocumentProcessingRequest

@Controller("document-processing")
class DocumentProcessingController:
    def __init__(self, document_processing_service: DocumentProcessingService):
        self.document_processing_service = document_processing_service
        self.ALLOWED_MODELS = [
            "openai",
            "llava-llama3",
            "llama-90b",
            "zephyr-7b",
            "gemma-9b",
            "llama-3b",
            "llama-70b"
        ]
        self.DEFAULT_MODEL = "llama-90b"  # Cambiado a llama-90b como default

    @Post("/process")
    async def process_document(
        self,
        file: UploadFile = File(..., description="Archivo PDF a procesar"),
        topic: str = Form(..., description="Tema específico para el resumen"),
        model_type: str = Form("llama-90b", description="Modelo a utilizar para el procesamiento"),  # Cambiado el default
        temperature: float = Form(0.7, ge=0.0, le=1.0, description="Temperatura para generación de texto"),
        chunk_size: Optional[int] = Form(1000, ge=100, description="Tamaño de los chunks de texto"),
        chunk_overlap: Optional[int] = Form(200, ge=0, description="Superposición entre chunks"),
        min_summary_length: Optional[int] = Form(2000, ge=500, description="Longitud mínima del resumen"),
        max_summary_length: Optional[int] = Form(5000, ge=1000, description="Longitud máxima del resumen"),
        include_examples: bool = Form(True, description="Incluir ejemplos en el resumen"),
        session: AsyncSession = Depends(config.get_db)
    ) -> DocumentProcessingResponse:
        """
        Procesa un documento PDF y genera un resumen basado en el tema especificado.

        Modelos disponibles:
        - openai: OpenAI GPT
        - llava-llama3: Llava Llama3 local
        - llama-90b: Meta Llama 3.2 90B Vision Instruct
        - zephyr-7b: Hugging Face Zephyr 7B
        - gemma-9b: Google Gemma 2 9B
        - llama-3b: Meta Llama 3.2 3B Instruct
        - llama-70b: Meta Llama 3.1 70B Instruct
        """
        # Validar el tipo de archivo
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Solo se permiten archivos PDF"
            )

        # Validar el modelo
        if model_type not in self.ALLOWED_MODELS:
            raise HTTPException(
                status_code=400,
                detail=f"Modelo no soportado. Use uno de: {', '.join(self.ALLOWED_MODELS)}"
            )

        # Validar longitudes de resumen
        if min_summary_length and max_summary_length and min_summary_length >= max_summary_length:
            raise HTTPException(
                status_code=400,
                detail="min_summary_length debe ser menor que max_summary_length"
            )

        try:
            process_request = DocumentProcessingRequest(
                model_type=model_type,
                temperature=temperature,
                min_summary_length=min_summary_length,
                max_summary_length=max_summary_length,
                include_examples=include_examples,
                topic=topic
            )

            return await self.document_processing_service.process_document(
                file=file,
                topic=topic,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                session=session,
                process_request=process_request
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error procesando el documento: {str(e)}"
            )

    @Post("/models")
    async def get_available_models(self) -> dict:
        """Retorna la lista de modelos disponibles y sus configuraciones"""
        return {
            "available_models": self.ALLOWED_MODELS,
            "default_model": self.DEFAULT_MODEL,
            "models_info": {
                "openai": "OpenAI GPT",
                "llava-llama3": "Llava Llama3 local",
                "llama-90b": "Meta Llama 3.2 90B Vision Instruct",
                "zephyr-7b": "Hugging Face Zephyr 7B",
                "gemma-9b": "Google Gemma 2 9B",
                "llama-3b": "Meta Llama 3.2 3B Instruct",
                "llama-70b": "Meta Llama 3.1 70B Instruct"
            },
            "configurations": {
                "temperature_range": {"min": 0.0, "max": 1.0, "default": 0.7},
                "chunk_size": {"min": 100, "default": 1000},
                "chunk_overlap": {"min": 0, "default": 200},
                "summary_length": {
                    "min": 500,
                    "default_min": 2000,
                    "default_max": 5000
                }
            }
        }