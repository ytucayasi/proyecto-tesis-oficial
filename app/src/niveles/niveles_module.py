from nest.core import Module
from .niveles_controller import NivelesController
from .niveles_service import NivelesService

@Module(
    controllers=[NivelesController],
    providers=[NivelesService],
    imports=[]
)
class NivelesModule:
    pass
