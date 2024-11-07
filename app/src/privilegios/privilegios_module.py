from nest.core import Module
from .privilegios_controller import PrivilegiosController
from .privilegios_service import PrivilegiosService

@Module(
    controllers=[PrivilegiosController],
    providers=[PrivilegiosService],
    imports=[]
)   
class PrivilegiosModule:
    pass
