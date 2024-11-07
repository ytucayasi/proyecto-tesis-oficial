from nest.core import Module
from .unidad_controller import UnidadController
from .unidad_service import UnidadService

@Module(
    controllers=[UnidadController],
    providers=[UnidadService]
)
class UnidadModule:
    pass

# __init__.py
from .unidad_module import UnidadModule
from .unidad_controller import UnidadController
from .unidad_service import UnidadService
from .unidad_entity import UnidadEntity
from .unidad_model import Unidad, UnidadResponse, UpdateUnidad

__all__ = [
    'UnidadModule',
    'UnidadController',
    'UnidadService',
    'UnidadEntity',
    'Unidad',
    'UnidadResponse',
    'UpdateUnidad'
]