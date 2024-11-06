from nest.core import Controller, Get, Post, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config


from .ejemplos_service import EjemplosService
from .ejemplos_model import Ejemplos


@Controller("ejemplos")
class EjemplosController:

    def __init__(self, ejemplos_service: EjemplosService):
        self.ejemplos_service = ejemplos_service

    @Get("/")
    async def get_ejemplos(self, session: AsyncSession = Depends(config.get_db)):
        return await self.ejemplos_service.get_ejemplos(session)

    @Post("/")
    async def add_ejemplos(self, ejemplos: Ejemplos, session: AsyncSession = Depends(config.get_db)):
        return await self.ejemplos_service.add_ejemplos(ejemplos, session)
 