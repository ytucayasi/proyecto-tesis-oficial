from nest.core import Module
from .roles_controller import RolesController
from .roles_service import RolesService

@Module(
    controllers=[RolesController],
    providers=[RolesService],
    imports=[]
)   
class RolesModule:
    pass
