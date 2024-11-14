from nest.core import Injectable
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import os
import re
from datetime import datetime
from langchain_community.vectorstores import Chroma
from .document_processing_model import DocumentProcessingResponse, DocumentProcessingRequest
from .document_processing_entity import DocumentProcessingEntity
from .model_configs import MODEL_CONFIGS
from .prompt_handlers import generate_prompt_templates, generate_topic_query
from .document_processors import process_pdf, identify_sections
from .embedding_handlers import initialize_embeddings
from .llm_handlers import get_llm
from .summary_handlers import generate_summary

@Injectable()
class DocumentProcessingService:
    def __init__(self):
        self.UPLOAD_DIR = "uploads"
        self.SUMMARY_DIR = "summaries"
        self.persist_directory = "chroma_db"
        self.MODEL_CONFIGS = MODEL_CONFIGS
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.SUMMARY_DIR, exist_ok=True)
        os.makedirs(self.persist_directory, exist_ok=True)

    async def process_document(
        self,
        file: UploadFile,
        topic: str,
        chunk_size: int,
        chunk_overlap: int,
        session: AsyncSession,
        process_request: DocumentProcessingRequest
    ) -> DocumentProcessingResponse:
        import time
        start_time = time.time()
        file_path = None
        sections = {}
        
        try:
            # Procesar PDF y generar embeddings
            texts = await process_pdf(file)
            if not texts:
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo extraer texto del PDF"
                )
            
            # Identificar secciones si no hay topic específico
            if topic:
                sections = {"Resumen por Tema": [topic]}
            else:
                sections = identify_sections(texts)

            # Inicializar embeddings y crear vectorstore
            embeddings = initialize_embeddings()
            
            # Almacenar en ChromaDB
            db = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=self.persist_directory
            )
            
            # Generar query y obtener chunks relevantes
            query = generate_topic_query(topic)
            relevant_chunks = db.similarity_search(query, k=8)
            
            # Obtener LLM
            llm = get_llm(process_request)
            
            # Generar resumen
            summary = await generate_summary(relevant_chunks, topic, llm)

            # Calcular tiempo de procesamiento
            processing_time = time.time() - start_time

            # Obtener lista de archivos existentes y generar nuevo nombre
            existing_files = os.listdir(self.SUMMARY_DIR)
            summary_numbers = [
                int(re.search(r"_summary_(\d+)\.txt$", f).group(1))
                for f in existing_files if re.search(r"_summary_(\d+)\.txt$", f)
            ]
            summary_counter = max(summary_numbers, default=0) + 1

            # Guardar el resumen con nombre único
            summary_path = os.path.join(self.SUMMARY_DIR, f"{file.filename}_summary_{summary_counter}.txt")
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(summary)

            # Guardar en BD
            doc_processing = DocumentProcessingEntity(
                original_filename=file.filename,
                summary_path=summary_path,
                summary_content=summary,
                topic=topic,
                model_used=process_request.model_type,
                processing_metadata={
                    "temperature": process_request.temperature,
                    "min_summary_length": getattr(process_request, "min_summary_length", None),
                    "max_summary_length": getattr(process_request, "max_summary_length", None),
                    "include_examples": getattr(process_request, "include_examples", True)
                },
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                num_chunks=len(texts) if texts else None,
                processing_time=processing_time
            )

            session.add(doc_processing)
            await session.commit()
            await session.refresh(doc_processing)

            return DocumentProcessingResponse(
                summary=summary,
                file_path=summary_path,
                metadata={
                    "original_file": file.filename,
                    "chunk_size": chunk_size,
                    "chunk_overlap": chunk_overlap,
                    "num_chunks": len(texts) if texts else None,
                    "processing_time": processing_time,
                    "model_parameters": {
                        "temperature": process_request.temperature,
                        "min_length": getattr(process_request, "min_summary_length", None),
                        "max_length": getattr(process_request, "max_summary_length", None)
                    }
                },
                created_at=doc_processing.created_at,
                model_used=process_request.model_type,
                sections_found=list(sections.keys()) if sections else [],
                topic_covered=topic
            )

        except Exception as e:
            print(f"Error processing document: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))