from nest.core import Module
from .historial_recurso_controller import HistorialRecursoController
from .historial_recurso_service import HistorialRecursoService

@Module(
    controllers=[HistorialRecursoController],
    providers=[HistorialRecursoService]
)
class HistorialRecursoModule:
    pass