from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .usuario_roles_service import UsuarioRolesService
from .usuario_roles_model import UsuarioRoles, UpdateUsuarioRoles

@Controller("usuario_roles")
class UsuarioRolesController:

    def __init__(self, usuario_roles_service: UsuarioRolesService):
        self.usuario_roles_service = usuario_roles_service

    @Get("/")
    async def get_usuario_roles(self, session: AsyncSession = Depends(config.get_db)):
        return await self.usuario_roles_service.get_usuario_roles(session)

    @Get("/{usuario_rol_id}")
    async def get_usuario_rol_by_id(self, usuario_rol_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.usuario_roles_service.get_usuario_rol_by_id(usuario_rol_id, session)

    @Post("/")
    async def add_usuario_rol(self, usuario_rol: UsuarioRoles, session: AsyncSession = Depends(config.get_db)):
        return await self.usuario_roles_service.add_usuario_rol(usuario_rol, session)

    @Put("/{usuario_rol_id}")
    async def update_usuario_rol(self, usuario_rol_id: int, usuario_rol_update: UpdateUsuarioRoles, session: AsyncSession = Depends(config.get_db)):
        return await self.usuario_roles_service.update_usuario_rol(usuario_rol_id, usuario_rol_update, session)

    @Delete("/{usuario_rol_id}")
    async def delete_usuario_rol(self, usuario_rol_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.usuario_roles_service.delete_usuario_rol(usuario_rol_id, session)
