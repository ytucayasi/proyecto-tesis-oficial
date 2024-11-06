from nest.core import Module
from .programas_controller import ProgramasController
from .programas_service import ProgramasService

@Module(
    controllers=[ProgramasController],
    providers=[ProgramasService],
    imports=[]
)
class ProgramasModule:
    pass
