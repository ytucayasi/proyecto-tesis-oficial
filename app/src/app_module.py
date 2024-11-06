from nest.core import PyNestFactory, Module
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.users.users_module import UsersModule
from src.ejemplos.ejemplos_module import EjemplosModule
from src.personas.personas_module import PersonasModule
from src.facultades.facultades_module import FacultadesModule


@Module(
    imports=[UsersModule, EjemplosModule, PersonasModule, FacultadesModule],
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
