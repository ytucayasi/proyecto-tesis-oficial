from .generacion_recurso_model import GeneracionRecurso
from nest.core import Injectable


@Injectable
class GeneracionRecursoService:

    def __init__(self):
        self.database = []
        
    def get_generacion_recurso(self):
        return self.database
    
    def add_generacion_recurso(self, generacion_recurso: GeneracionRecurso):
        self.database.append(generacion_recurso)
        return generacion_recurso
