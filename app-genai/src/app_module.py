from nest.core import PyNestFactory, Module
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.document_processing.document_processing_module import DocumentProcessingModule
from fastapi.middleware.cors import CORSMiddleware
from src.resource_generation.resource_generation_module import ResourceGenerationModule
from src.resource.resource_module import ResourceModule
            

@Module(
    imports=[DocumentProcessingModule, ResourceGenerationModule, ResourceModule],
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
http_server.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Reemplaza con la URL de tu aplicación Angular
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

@http_server.on_event("startup")
async def startup():
    await config.create_all()
