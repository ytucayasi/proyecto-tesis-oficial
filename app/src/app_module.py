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
from src.facultades.facultades_module import FacultadesModule
from src.niveles.niveles_module import NivelesModule
from src.escuelas_profesionales.escuelas_profesionales_module import (
    EscuelasProfesionalesModule,
)
from src.planes_academicos.planes_academicos_module import PlanesAcademicosModule
from src.programas.programas_module import ProgramasModule
from src.ciclos.ciclos_module import CiclosModule
from src.cursos.cursos_module import CursosModule
from src.ciclos_cursos.ciclos_cursos_module import CiclosCursosModule
from src.unidad.unidad_module import UnidadModule
from src.sesion_aprendizaje.sesion_aprendizaje_module import SesionAprendizajeModule
from src.tipo_secuencia.tipo_secuencia_module import TipoSecuenciaModule
from src.secuencia_aprendizaje.secuencia_aprendizaje_module import (
    SecuenciaAprendizajeModule,
)


@Module(
    imports=[
        UsersModule,
        EjemplosModule,
        PersonasModule,
        InputModule,
        GeneracionRecursoModule,
        DisenoPdfModule,
        FacultadesModule,
        NivelesModule,
        EscuelasProfesionalesModule,
        PlanesAcademicosModule,
        ProgramasModule,
        CiclosModule,
        CursosModule,
        CiclosCursosModule,
        UnidadModule,
        SesionAprendizajeModule,
        TipoSecuenciaModule,
        SecuenciaAprendizajeModule,
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
