from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .usuarios_service import UsuariosService
from .usuarios_model import Usuarios, UpdateUsuarios

@Controller("usuarios")
class UsuariosController:

    def __init__(self, usuarios_service: UsuariosService):
        self.usuarios_service = usuarios_service

    @Get("/")
    async def get_usuarios(self, session: AsyncSession = Depends(config.get_db)):
        return await self.usuarios_service.get_usuarios(session)

    @Get("/{usuario_id}")
    async def get_usuario_by_id(self, usuario_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.usuarios_service.get_usuario_by_id(usuario_id, session)

    @Post("/")
    async def add_usuario(self, usuario: Usuarios, session: AsyncSession = Depends(config.get_db)):
        return await self.usuarios_service.add_usuario(usuario, session)

    @Put("/{usuario_id}")
    async def update_usuario(self, usuario_id: int, usuario_update: UpdateUsuarios, session: AsyncSession = Depends(config.get_db)):
        return await self.usuarios_service.update_usuario(usuario_id, usuario_update, session)

    @Delete("/{usuario_id}")
    async def delete_usuario(self, usuario_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.usuarios_service.delete_usuario(usuario_id, session)
