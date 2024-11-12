from nest.core import PyNestFactory, Module
from .config import config
from .app_controller import AppController
from .app_service import AppService
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
from src.curso_usuario.curso_usuario_module import CursoUsuarioModule
from src.historial_recurso.historial_recurso_module import HistorialRecursoModule


@Module(
    imports=[
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
        CursoUsuarioModule,
        HistorialRecursoModule,
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