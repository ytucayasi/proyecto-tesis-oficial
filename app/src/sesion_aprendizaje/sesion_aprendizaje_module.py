from nest.core import Module
from .sesion_aprendizaje_controller import SesionAprendizajeController
from .sesion_aprendizaje_service import SesionAprendizajeService

@Module(
    controllers=[SesionAprendizajeController],
    providers=[SesionAprendizajeService]
)
class SesionAprendizajeModule:
    pass