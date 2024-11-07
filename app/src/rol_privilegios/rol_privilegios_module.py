from nest.core import Module
from .rol_privilegios_controller import RolPrivilegiosController
from .rol_privilegios_service import RolPrivilegiosService

@Module(
    controllers=[RolPrivilegiosController],
    providers=[RolPrivilegiosService],
    imports=[]
)   
class RolPrivilegiosModule:
    pass
