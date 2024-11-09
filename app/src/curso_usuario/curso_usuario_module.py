from nest.core import Module
from .curso_usuario_controller import CursoUsuarioController
from .curso_usuario_service import CursoUsuarioService

@Module(
    controllers=[CursoUsuarioController],
    providers=[CursoUsuarioService]
)
class CursoUsuarioModule:
    pass