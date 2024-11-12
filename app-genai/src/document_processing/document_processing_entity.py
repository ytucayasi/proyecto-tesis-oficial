from src.config import config
from sqlalchemy import Integer, String, DateTime, Text
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
        return f"DocumentProcessing(processing_id={self.processing_id}, original_filename='{self.original_filename}')"