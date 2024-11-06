from nest.core import Module
from .cursos_controller import CursosController
from .cursos_service import CursosService

@Module(
    controllers=[CursosController],
    providers=[CursosService],
    imports=[]
)
class CursosModule:
    pass
