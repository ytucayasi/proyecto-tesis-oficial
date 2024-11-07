from nest.core import PyNestFactory, Module
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.users.users_module import UsersModule
from src.ejemplos.ejemplos_module import EjemplosModule
from src.personas.personas_module import PersonasModule
from src.input.input_module import InputModule
from src.generacion_recurso.generacion_recurso_module import GeneracionRecursoModule
from src.diseno_pdf.diseno_pdf_module import DisenoPdfModule


@Module(
    imports=[
        UsersModule,
        EjemplosModule,
        PersonasModule,
        InputModule,
        GeneracionRecursoModule,
        DisenoPdfModule,
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
