from nest.core import Module
from .equivalencia_replicadas_controller import EquivalenciaReplicadasController
from .equivalencia_replicadas_service import EquivalenciaReplicadasService

@Module(
    controllers=[EquivalenciaReplicadasController],
    providers=[EquivalenciaReplicadasService],
    imports=[]
)   
class EquivalenciaReplicadasModule:
    pass
