from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .roles_service import RolesService
from .roles_model import Roles, UpdateRoles

@Controller("roles")
class RolesController:

    def __init__(self, roles_service: RolesService):
        self.roles_service = roles_service

    @Get("/")
    async def get_roles(self, session: AsyncSession = Depends(config.get_db)):
        return await self.roles_service.get_roles(session)

    @Get("/{rol_id}")
    async def get_rol_by_id(self, rol_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.roles_service.get_rol_by_id(rol_id, session)

    @Post("/")
    async def add_rol(self, rol: Roles, session: AsyncSession = Depends(config.get_db)):
        return await self.roles_service.add_rol(rol, session)

    @Put("/{rol_id}")
    async def update_rol(self, rol_id: int, rol_update: UpdateRoles, session: AsyncSession = Depends(config.get_db)):
        return await self.roles_service.update_rol(rol_id, rol_update, session)

    @Delete("/{rol_id}")
    async def delete_rol(self, rol_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.roles_service.delete_rol(rol_id, session)
