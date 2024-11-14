from nest.core import Module
from .resource_generation_controller import ResourceGenerationController
from .resource_generation_service import ResourceGenerationService


@Module(
    controllers=[ResourceGenerationController],
    providers=[ResourceGenerationService],
    imports=[]
)   
class ResourceGenerationModule:
    pass

    