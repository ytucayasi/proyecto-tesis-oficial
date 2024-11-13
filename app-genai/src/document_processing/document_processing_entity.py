from src.config import config
from sqlalchemy import Integer, String, DateTime, Text, JSON, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class DocumentProcessingEntity(config.Base):
    __tablename__ = "document_processing"

    processing_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    
    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    summary_path: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    summary_content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    
    topic: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    model_used: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    processing_metadata: Mapped[dict] = mapped_column(
        JSON,
        nullable=True,
        default={}
    )

    chunk_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1000
    )

    chunk_overlap: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=200
    )

    num_chunks: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    processing_time: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    def __repr__(self) -> str:
        return (
            f"DocumentProcessing("
            f"processing_id={self.processing_id}, "
            f"original_filename='{self.original_filename}', "
            f"topic='{self.topic}', "
            f"model='{self.model_used}')"
        )

    def to_dict(self) -> dict:
        """Convierte la entidad a un diccionario para respuestas API"""
        return {
            "processing_id": self.processing_id,
            "original_filename": self.original_filename,
            "summary_path": self.summary_path,
            "topic": self.topic,
            "model_used": self.model_used,
            "processing_metadata": self.processing_metadata,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "num_chunks": self.num_chunks,
            "processing_time": self.processing_time,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }