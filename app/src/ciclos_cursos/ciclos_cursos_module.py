from nest.core import Module
from .ciclos_cursos_controller import CiclosCursosController
from .ciclos_cursos_service import CiclosCursosService

@Module(
    controllers=[CiclosCursosController],
    providers=[CiclosCursosService],
    imports=[]
)
class CiclosCursosModule:
    pass
