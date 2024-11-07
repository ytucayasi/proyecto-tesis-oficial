from nest.core import Module
from .usuario_roles_controller import UsuarioRolesController
from .usuario_roles_service import UsuarioRolesService

@Module(
    controllers=[UsuarioRolesController],
    providers=[UsuarioRolesService],
    imports=[]
)   
class UsuarioRolesModule:
    pass
