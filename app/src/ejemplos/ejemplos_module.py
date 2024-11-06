from nest.core import Module
from .ejemplos_controller import EjemplosController
from .ejemplos_service import EjemplosService


@Module(
    controllers=[EjemplosController],
    providers=[EjemplosService],
    imports=[]
)   
class EjemplosModule:
    pass

    