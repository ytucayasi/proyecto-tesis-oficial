from nest.core import Module
from .resource_controller import ResourceController
from .resource_service import ResourceService


@Module(
    controllers=[ResourceController],
    providers=[ResourceService],
    imports=[]
)   
class ResourceModule:
    pass

    