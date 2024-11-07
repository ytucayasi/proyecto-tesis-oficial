from nest.core import Module
from .curso_equivalencias_controller import CursoEquivalenciasController
from .curso_equivalencias_service import CursoEquivalenciasService

@Module(
    controllers=[CursoEquivalenciasController],
    providers=[CursoEquivalenciasService],
    imports=[]
)   
class CursoEquivalenciasModule:
    pass
