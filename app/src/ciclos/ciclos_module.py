from nest.core import Module
from .ciclos_controller import CiclosController
from .ciclos_service import CiclosService

@Module(
    controllers=[CiclosController],
    providers=[CiclosService],
    imports=[]
)
class CiclosModule:
    pass
