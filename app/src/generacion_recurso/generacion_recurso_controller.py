from nest.core import Controller, Get, Post
from .generacion_recurso_service import GeneracionRecursoService
from .generacion_recurso_model import GeneracionRecurso


@Controller("generacion_recurso")
class GeneracionRecursoController:

    def __init__(self, generacion_recurso_service: GeneracionRecursoService):
        self.generacion_recurso_service = generacion_recurso_service
    
    @Get("/")
    def get_generacion_recurso(self):
        return self.generacion_recurso_service.get_generacion_recurso()
        
    @Post("/")
    def add_generacion_recurso(self, generacion_recurso: GeneracionRecurso):
        return self.generacion_recurso_service.add_generacion_recurso(generacion_recurso)

