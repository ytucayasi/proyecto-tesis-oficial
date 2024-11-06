from nest.core import Module
from .personas_controller import PersonasController
from .personas_service import PersonasService

@Module(
    controllers=[PersonasController],
    providers=[PersonasService],
    imports=[]
)   
class PersonasModule:
    pass