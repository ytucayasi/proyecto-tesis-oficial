from nest.core import Module
from .sesiones_controller import SesionesController
from .sesiones_service import SesionesService

@Module(
    controllers=[SesionesController],
    providers=[SesionesService],
    imports=[]
)   
class SesionesModule:
    pass
