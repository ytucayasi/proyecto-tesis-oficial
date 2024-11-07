from nest.core import Module
from .generacion_recurso_controller import GeneracionRecursoController
from .generacion_recurso_service import GeneracionRecursoService


@Module(
    controllers=[GeneracionRecursoController],
    providers=[GeneracionRecursoService],
    imports=[]
)   
class GeneracionRecursoModule:
    pass

    