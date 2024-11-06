from nest.core import Module
from .escuelas_profesionales_controller import EscuelasProfesionalesController
from .escuelas_profesionales_service import EscuelasProfesionalesService

@Module(
    controllers=[EscuelasProfesionalesController],
    providers=[EscuelasProfesionalesService],
    imports=[]
)
class EscuelasProfesionalesModule:
    pass
