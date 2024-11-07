from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .rol_privilegios_service import RolPrivilegiosService
from .rol_privilegios_model import RolPrivilegios, UpdateRolPrivilegios

@Controller("rol_privilegios")
class RolPrivilegiosController:

    def __init__(self, rol_privilegios_service: RolPrivilegiosService):
        self.rol_privilegios_service = rol_privilegios_service

    @Get("/")
    async def get_rol_privilegios(self, session: AsyncSession = Depends(config.get_db)):
        return await self.rol_privilegios_service.get_rol_privilegios(session)

    @Get("/{rol_privilegio_id}")
    async def get_rol_privilegio_by_id(self, rol_privilegio_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.rol_privilegios_service.get_rol_privilegio_by_id(rol_privilegio_id, session)

    @Post("/")
    async def add_rol_privilegio(self, rol_privilegio: RolPrivilegios, session: AsyncSession = Depends(config.get_db)):
        return await self.rol_privilegios_service.add_rol_privilegio(rol_privilegio, session)

    @Put("/{rol_privilegio_id}")
    async def update_rol_privilegio(self, rol_privilegio_id: int, rol_privilegio_update: UpdateRolPrivilegios, session: AsyncSession = Depends(config.get_db)):
        return await self.rol_privilegios_service.update_rol_privilegio(rol_privilegio_id, rol_privilegio_update, session)

    @Delete("/{rol_privilegio_id}")
    async def delete_rol_privilegio(self, rol_privilegio_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.rol_privilegios_service.delete_rol_privilegio(rol_privilegio_id, session)
