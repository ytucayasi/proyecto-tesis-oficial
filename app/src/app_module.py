from nest.core import PyNestFactory, Module
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.personas.personas_module import PersonasModule
from src.usuarios.usuarios_module import UsuariosModule
from src.usuario_roles.usuario_roles_module import UsuarioRolesModule
from src.roles.roles_module import RolesModule
from src.rol_privilegios.rol_privilegios_module import RolPrivilegiosModule
from src.privilegios.privilegios_module import PrivilegiosModule
from src.sesiones.sesiones_module import SesionesModule
from src.evaluaciones.evaluaciones_module import EvaluacionesModule
from src.curso_equivalencias.curso_equivalencias_module import CursoEquivalenciasModule
from src.equivalencia_replicadas.equivalencia_replicadas_module import (
    EquivalenciaReplicadasModule,
)


@Module(
    imports=[
        PersonasModule,
        UsuariosModule,
        UsuarioRolesModule,
        RolesModule,
        RolPrivilegiosModule,
        PrivilegiosModule,
        SesionesModule,
        EvaluacionesModule,
        CursoEquivalenciasModule,
        EquivalenciaReplicadasModule,
    ],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="This is my Async PyNest app.",
    title="PyNest Application",
    version="1.0.0",
    debug=True,
)
http_server = app.get_server()


@http_server.on_event("startup")
async def startup():
    await config.create_all()
