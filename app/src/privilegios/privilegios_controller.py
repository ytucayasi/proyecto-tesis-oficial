from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .privilegios_service import PrivilegiosService
from .privilegios_model import Privilegios, UpdatePrivilegios

@Controller("privilegios")
class PrivilegiosController:

    def __init__(self, privilegios_service: PrivilegiosService):
        self.privilegios_service = privilegios_service

    @Get("/")
    async def get_privilegios(self, session: AsyncSession = Depends(config.get_db)):
        return await self.privilegios_service.get_privilegios(session)

    @Get("/{privilegio_id}")
    async def get_privilegio_by_id(self, privilegio_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.privilegios_service.get_privilegio_by_id(privilegio_id, session)

    @Post("/")
    async def add_privilegio(self, privilegio: Privilegios, session: AsyncSession = Depends(config.get_db)):
        return await self.privilegios_service.add_privilegio(privilegio, session)

    @Put("/{privilegio_id}")
    async def update_privilegio(self, privilegio_id: int, privilegio_update: UpdatePrivilegios, session: AsyncSession = Depends(config.get_db)):
        return await self.privilegios_service.update_privilegio(privilegio_id, privilegio_update, session)

    @Delete("/{privilegio_id}")
    async def delete_privilegio(self, privilegio_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.privilegios_service.delete_privilegio(privilegio_id, session)
