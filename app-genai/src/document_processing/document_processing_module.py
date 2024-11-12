from nest.core import Module
from .document_processing_controller import DocumentProcessingController
from .document_processing_service import DocumentProcessingService

@Module(
    controllers=[DocumentProcessingController],
    providers=[DocumentProcessingService]
)
class DocumentProcessingModule:
    pass