from nest.core import Module
from .diseno_pdf_controller import DisenoPdfController
from .diseno_pdf_service import DisenoPdfService

@Module(
    controllers=[DisenoPdfController],
    providers=[DisenoPdfService],
    imports=[]
)
class DisenoPdfModule:
    pass