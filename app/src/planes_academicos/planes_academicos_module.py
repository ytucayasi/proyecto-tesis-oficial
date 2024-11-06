from nest.core import Module
from .planes_academicos_controller import PlanesAcademicosController
from .planes_academicos_service import PlanesAcademicosService

@Module(
    controllers=[PlanesAcademicosController],
    providers=[PlanesAcademicosService],
    imports=[]
)
class PlanesAcademicosModule:
    pass
