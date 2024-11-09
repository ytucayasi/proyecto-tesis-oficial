from nest.core import Module
from .secuencia_aprendizaje_controller import SecuenciaAprendizajeController
from .secuencia_aprendizaje_service import SecuenciaAprendizajeService

@Module(
    controllers=[SecuenciaAprendizajeController],
    providers=[SecuenciaAprendizajeService]
)
class SecuenciaAprendizajeModule:
    pass