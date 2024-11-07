from nest.core import Module
from .facultades_controller import FacultadesController
from .facultades_service import FacultadesService


@Module(
    controllers=[FacultadesController],
    providers=[FacultadesService],
    imports=[]
)   
class FacultadesModule:
    pass