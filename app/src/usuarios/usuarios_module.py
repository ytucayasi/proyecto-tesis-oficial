from nest.core import Module
from .usuarios_controller import UsuariosController
from .usuarios_service import UsuariosService

@Module(
    controllers=[UsuariosController],
    providers=[UsuariosService],
    imports=[]
)   
class UsuariosModule:
    pass