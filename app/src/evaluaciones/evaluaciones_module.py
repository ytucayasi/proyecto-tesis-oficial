from nest.core import Module
from .evaluaciones_controller import EvaluacionesController
from .evaluaciones_service import EvaluacionesService

@Module(
    controllers=[EvaluacionesController],
    providers=[EvaluacionesService],
    imports=[]
)   
class EvaluacionesModule:
    pass
