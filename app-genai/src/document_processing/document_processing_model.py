from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Literal, List, Union

class DocumentProcessingRequest(BaseModel):
    model_type: Literal[
        "openai",
        "llava-llama3",
        "llama-90b",
        "zephyr-7b",
        "gemma-9b",
        "llama-3b",
        "llama-70b"
    ] = Field(
        default="llama-90b",
        description="Modelo a utilizar para el procesamiento"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Temperatura para la generación del texto"
    )
    min_summary_length: Optional[int] = Field(
        default=2000,
        ge=500,
        description="Longitud mínima del resumen en caracteres"
    )
    max_summary_length: Optional[int] = Field(
        default=5000,
        ge=1000,
        description="Longitud máxima del resumen en caracteres"
    )
    include_examples: bool = Field(
        default=True,
        description="Incluir ejemplos en el resumen"
    )
    topic: str = Field(
        ...,  # Hace que sea requerido
        min_length=3,
        description="Tema específico para el resumen"
    )

class DocumentMetadata(BaseModel):
    original_file: str
    chunk_size: int
    chunk_overlap: int
    num_chunks: int
    file_size: Optional[int] = None
    processing_time: Optional[float] = None
    model_parameters: Optional[Dict[str, Union[str, int, float]]] = None

class DocumentProcessingResponse(BaseModel):
    summary: str = Field(..., description="Resumen generado")
    file_path: str = Field(..., description="Ruta del archivo de resumen")
    metadata: DocumentMetadata
    created_at: datetime
    model_used: str
    sections_found: List[str] = Field(default_factory=list)
    topic_covered: str = Field(..., description="Tema cubierto en el resumen")
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "summary": "Este es un resumen ejemplo...",
                "file_path": "/path/to/summary.txt",
                "metadata": {
                    "original_file": "document.pdf",
                    "chunk_size": 1000,
                    "chunk_overlap": 200,
                    "num_chunks": 15,
                    "file_size": 1024000,
                    "processing_time": 5.23,
                    "model_parameters": {
                        "temperature": 0.7,
                        "min_length": 2000,
                        "max_length": 5000
                    }
                },
                "created_at": "2024-11-13T12:00:00",
                "model_used": "llama-90b",
                "sections_found": ["Introducción", "Desarrollo", "Conclusión"],
                "topic_covered": "Inteligencia Artificial"
            }
        }