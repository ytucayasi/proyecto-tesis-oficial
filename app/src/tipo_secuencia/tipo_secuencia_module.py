from nest.core import Module
from .tipo_secuencia_controller import TipoSecuenciaController
from .tipo_secuencia_service import TipoSecuenciaService

@Module(
    controllers=[TipoSecuenciaController],
    providers=[TipoSecuenciaService]
)
class TipoSecuenciaModule:
    pass