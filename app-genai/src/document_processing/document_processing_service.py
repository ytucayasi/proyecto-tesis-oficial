from nest.core import Injectable
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, List
import os
import re
import tempfile
from datetime import datetime
from .document_processing_model import DocumentProcessingResponse, DocumentProcessingRequest
from .document_processing_entity import DocumentProcessingEntity
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import OpenAI, Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate
from .llm_custom import OpenRouterLLM

@Injectable()
class DocumentProcessingService:
    def __init__(self):
        self.UPLOAD_DIR = "uploads"
        self.SUMMARY_DIR = "summaries"
        self.persist_directory = "chroma_db"
        self.MODEL_CONFIGS = {
            "openai": {
                "requires_api_key": True,
                "api_key_env": "OPENAI_API_KEY",
                "base_url": None,
                "model_name": None
            },
            "llava-llama3": {
                "requires_api_key": False,
                "api_key_env": None,
                "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                "model_name": "llava-llama3:latest"
            },
            # OpenRouter models
            "llama-90b": {
                "requires_api_key": True,
                "api_key_env": "OPENROUTER_API_KEY",
                "base_url": "https://openrouter.ai/api/v1",
                "model_name": "meta-llama/llama-3.2-90b-vision-instruct:free",
                "is_openrouter": True,
                "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
                "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
            },
            "zephyr-7b": {
                "requires_api_key": True,
                "api_key_env": "OPENROUTER_API_KEY",
                "base_url": "https://openrouter.ai/api/v1",
                "model_name": "huggingfaceh4/zephyr-7b-beta:free",
                "is_openrouter": True,
                "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
                "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
            },
            "gemma-9b": {
                "requires_api_key": True,
                "api_key_env": "OPENROUTER_API_KEY",
                "base_url": "https://openrouter.ai/api/v1",
                "model_name": "google/gemma-2-9b-it:free",
                "is_openrouter": True,
                "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
                "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
            },
            "llama-3b": {
                "requires_api_key": True,
                "api_key_env": "OPENROUTER_API_KEY",
                "base_url": "https://openrouter.ai/api/v1",
                "model_name": "meta-llama/llama-3.2-3b-instruct:free",
                "is_openrouter": True,
                "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
                "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
            },
            "llama-70b": {
                "requires_api_key": True,
                "api_key_env": "OPENROUTER_API_KEY",
                "base_url": "https://openrouter.ai/api/v1",
                "model_name": "meta-llama/llama-3.1-70b-instruct:free",
                "is_openrouter": True,
                "referer": os.getenv("OPENROUTER_REFERER", "http://localhost:8001"),
                "app_name": os.getenv("OPENROUTER_APP_NAME", "DocumentProcessingApp")
            }
        }
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.SUMMARY_DIR, exist_ok=True)
        os.makedirs(self.persist_directory, exist_ok=True)


    def _initialize_embeddings(self):
        try:
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        except Exception as e:
            print(f"Error initializing embeddings: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error initializing embeddings: {str(e)}"
            )

    def _get_llm(self, process_request: DocumentProcessingRequest):
        model_config = self.MODEL_CONFIGS.get(process_request.model_type)
        if not model_config:
            raise HTTPException(
                status_code=400,
                detail=f"Modelo no soportado: {process_request.model_type}"
            )

        if model_config["requires_api_key"]:
            api_key = os.getenv(model_config["api_key_env"])
            if not api_key:
                raise HTTPException(
                    status_code=500,
                    detail=f"API key no encontrada para {process_request.model_type}"
                )

        try:
            if process_request.model_type == "openai":
                return OpenAI(temperature=process_request.temperature)
            elif process_request.model_type == "llama-90b":
                return OpenRouterLLM(
                    base_url=model_config["base_url"],
                    api_key=os.getenv(model_config["api_key_env"]),
                    model=model_config["model_name"],
                    temperature=process_request.temperature,
                    referer=model_config.get("referer"),
                    app_name=model_config.get("app_name")
                )
            elif process_request.model_type == "zephyr-7b":
                return OpenRouterLLM(
                    base_url=model_config["base_url"],
                    api_key=os.getenv(model_config["api_key_env"]),
                    model=model_config["model_name"],
                    temperature=process_request.temperature,
                    referer=model_config.get("referer"),
                    app_name=model_config.get("app_name")
                )
            elif process_request.model_type == "gemma-9b":
                return OpenRouterLLM(
                    base_url=model_config["base_url"],
                    api_key=os.getenv(model_config["api_key_env"]),
                    model=model_config["model_name"],
                    temperature=process_request.temperature,
                    referer=model_config.get("referer"),
                    app_name=model_config.get("app_name")
                )
            elif process_request.model_type == "llama-3b":
                return OpenRouterLLM(
                    base_url=model_config["base_url"],
                    api_key=os.getenv(model_config["api_key_env"]),
                    model=model_config["model_name"],
                    temperature=process_request.temperature,
                    referer=model_config.get("referer"),
                    app_name=model_config.get("app_name")
                )
            elif process_request.model_type == "llama-70b":
                return OpenRouterLLM(
                    base_url=model_config["base_url"],
                    api_key=os.getenv(model_config["api_key_env"]),
                    model=model_config["model_name"],
                    temperature=process_request.temperature,
                    referer=model_config.get("referer"),
                    app_name=model_config.get("app_name")
                )
            else:
                return Ollama(
                    model=model_config["model_name"],
                    temperature=process_request.temperature,
                    base_url=model_config["base_url"]
                )
        except Exception as e:
            print(f"Error al inicializar modelo: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Error inicializando el modelo {process_request.model_type}: {str(e)}"
            )

    def _generate_prompt_templates(self, topic: str):
        """Genera los prompts adecuados según si hay topic o no"""
        map_template = """
        Analiza la siguiente información para generar un informe académico estructurado sobre {topic}:

        INFORMACIÓN:
        {text}

        Genera un análisis detallado siguiendo esta estructura:
        1. Conceptos principales
        2. Ejemplos relevantes
        3. Aplicaciones prácticas
        """

        combine_template = """
        Con base en los análisis previos, genera un informe académico estructurado:

        1. Título: {topic}
        ===
        2. Introducción:
        Presenta una introducción clara sobre {topic}, incluyendo su importancia y contexto en el campo de estudio.
        ===
        3. Contenido Principal:
        Desarrolla el contenido en detalle, incluyendo:
        - Conceptos fundamentales
        - Ejemplos prácticos
        - Casos de uso
        - Mejores prácticas
        ===
        4. Conclusión:
        Resume los puntos clave y proporciona una reflexión final sobre {topic}.

        INFORMACIÓN A PROCESAR:
        {text}
        """

        return (
            PromptTemplate(template=map_template, input_variables=["text", "topic"]),
            PromptTemplate(template=combine_template, input_variables=["text", "topic"])
        )

    def _identify_sections(self, texts) -> Dict[str, list]:
        """
        Identifica y agrupa textos por secciones.
        Detecta encabezados basándose en formato y longitud del texto.
        """
        sections = {"Contenido Principal": []}
        current_section = "Contenido Principal"
        
        for doc in texts:
            content = doc.page_content.strip()
            first_line = content.split('\n')[0].strip()
            
            # Mejorada la detección de encabezados
            is_heading = any([
                first_line.isupper(),
                first_line.startswith('#'),
                len(first_line) < 50 and first_line.endswith(':'),
                first_line.endswith('¶'),
                first_line.startswith('Capítulo'),
                first_line.startswith('Sección'),
                all(word[0].isupper() for word in first_line.split() if word)
            ])
            
            if is_heading:
                current_section = first_line
                if current_section not in sections:
                    sections[current_section] = []
            else:
                sections[current_section].append(doc)
        
        # Eliminar secciones vacías
        return {k: v for k, v in sections.items() if v}

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
            texts = await self._process_pdf(file)
            if not texts:
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo extraer texto del PDF"
                )
            
            # Identificar secciones si no hay topic específico
            if topic:
                sections = {"Resumen por Tema": [topic]}
            else:
                sections = self._identify_sections(texts)

            # Inicializar embeddings y crear vectorstore
            embeddings = self._initialize_embeddings()
            
            # Almacenar en ChromaDB
            db = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=self.persist_directory
            )
            
            # Obtener LLM
            llm = self._get_llm(process_request)
            
            # Generar resumen - Corregida esta parte
            query = self._generate_topic_query(topic)
            relevant_chunks = db.similarity_search(query, k=8)
            summary = await self._generate_summary(relevant_chunks, topic, process_request)
            
            # Calcular tiempo de procesamiento
            processing_time = time.time() - start_time

            # Guardar el resumen
            # summary_path = os.path.join(self.SUMMARY_DIR, f"{file.filename}_summary.txt")
            # with open(summary_path, "w", encoding="utf-8") as f:
            #     f.write(summary)

            # Obtener lista de archivos existentes en el directorio de resúmenes
            existing_files = os.listdir(self.SUMMARY_DIR)

            # Filtrar archivos que coincidan con el patrón y encontrar el número más alto actual
            summary_numbers = [
                int(re.search(r"_summary_(\d+)\.txt$", f).group(1))
                for f in existing_files if re.search(r"_summary_(\d+)\.txt$", f)
            ]

            # Determinar el siguiente número a utilizar
            summary_counter = max(summary_numbers, default=0) + 1

            # Guardar el resumen con un nombre único
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

    async def _process_pdf(self, file: UploadFile) -> List[Document]:
        try:
            content = await file.read()
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name

            loader = PDFPlumberLoader(temp_file_path)
            pages = loader.load()
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            
            chunks = text_splitter.split_documents(pages)
            return chunks
        
        finally:
            if 'temp_file_path' in locals():
                os.unlink(temp_file_path)

    async def _store_embeddings(self, texts: List[Document], embeddings) -> Chroma:
        try:
            vectorstore = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=self.persist_directory
            )
            vectorstore.persist()
            return vectorstore
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al almacenar embeddings: {str(e)}"
            )

    async def _retrieve_relevant_info(self, vectorstore: Chroma, topic: str) -> List[Document]:
        query = self._generate_topic_query(topic)
        try:
            return vectorstore.similarity_search(
                query,
                k=8,
                # fetch_k=20
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al recuperar información relevante: {str(e)}"
            )

    async def _generate_summary(
        self,
        relevant_chunks: List[Document],
        topic: str,
        process_request: DocumentProcessingRequest
    ) -> str:
        try:
            llm = self._get_llm(process_request)
            
            # Crear un prompt más directo para el modelo
            combined_text = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
            
            prompt = f"""
            Por favor, genera un resumen académico detallado sobre '{topic}' basado en el siguiente contenido.
            
            El resumen debe seguir esta estructura:
            1. Título: {topic}
            ===
            2. Introducción
            ===
            3. Contenido Principal
            - Conceptos fundamentales
            - Ejemplos prácticos
            - Casos de uso
            - Mejores prácticas
            ===
            4. Conclusión
            
            Contenido a analizar:
            {combined_text}
            """
            
            summary = llm(prompt)
            
            if not summary:
                raise HTTPException(
                    status_code=500,
                    detail="No se pudo generar un resumen"
                )
                
            return summary
            
        except Exception as e:
            print(f"Error en _generate_summary: {str(e)}")  # Debug
            raise HTTPException(
                status_code=500,
                detail=f"Error al generar el resumen: {str(e)}"
            )

    def _generate_topic_query(self, topic: str) -> str:
        return f"""
        Encuentra información relevante sobre '{topic}', incluyendo:
        - Definiciones y conceptos principales
        - Características y aspectos clave
        - Ejemplos y casos de uso
        - Detalles técnicos importantes
        - Mejores prácticas y recomendaciones
        """