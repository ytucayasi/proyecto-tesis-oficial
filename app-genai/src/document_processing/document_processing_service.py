from nest.core import Injectable
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import os
from datetime import datetime
from .document_processing_model import DocumentProcessingResponse
from .document_processing_entity import DocumentProcessingEntity
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain

@Injectable()
class DocumentProcessingService:
    def __init__(self):
        self.UPLOAD_DIR = "uploads"
        self.SUMMARY_DIR = "summaries"
        self.persist_directory = "chroma_db"
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.SUMMARY_DIR, exist_ok=True)
        os.makedirs(self.persist_directory, exist_ok=True)

    def _initialize_embeddings(self):
        try:
            # Usar un modelo más ligero y estable
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

    async def process_document(
        self,
        file: UploadFile,
        topic: Optional[str],
        chunk_size: int,
        chunk_overlap: int,
        session: AsyncSession
    ) -> DocumentProcessingResponse:
        file_path = os.path.join(self.UPLOAD_DIR, file.filename)
        try:
            # Guardar archivo
            content = await file.read()
            with open(file_path, "wb") as buffer:
                buffer.write(content)

            # Procesar PDF
            loader = PDFPlumberLoader(file_path)
            pages = loader.load()
            
            # Dividir texto
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", " ", ""]
            )
            texts = text_splitter.split_documents(pages)
            
            if not texts:
                raise HTTPException(
                    status_code=400,
                    detail="No se pudo extraer texto del PDF"
                )

            # Inicializar embeddings
            embeddings = self._initialize_embeddings()
            
            # Crear vectorstore
            db = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=self.persist_directory
            )
            
            # Verificar API key
            if not os.getenv('OPENAI_API_KEY'):
                raise HTTPException(
                    status_code=500,
                    detail="OPENAI_API_KEY no encontrada"
                )

            # Generar resumen
            llm = OpenAI(temperature=0.5)
            chain = load_summarize_chain(llm, chain_type="map_reduce")
            
            if topic:
                query = f"Genera un resumen sobre {topic} basado en el documento"
                relevant_docs = db.similarity_search(query, k=4)
                summary = chain.run(relevant_docs)
            else:
                summary = chain.run(texts)
            
            # Guardar resumen
            summary_path = os.path.join(self.SUMMARY_DIR, f"{file.filename}_summary.txt")
            with open(summary_path, "w", encoding="utf-8") as f:
                f.write(summary)

            # Guardar en BD
            doc_processing = DocumentProcessingEntity(
                original_filename=file.filename,
                summary_path=summary_path,
                summary_content=summary,
                topic=topic
            )
            session.add(doc_processing)
            await session.commit()
            await session.refresh(doc_processing)

            return DocumentProcessingResponse(
                summary=summary,
                file_path=summary_path,
                metadata={"original_file": file.filename},
                created_at=datetime.utcnow()
            )

        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Error processing document: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)