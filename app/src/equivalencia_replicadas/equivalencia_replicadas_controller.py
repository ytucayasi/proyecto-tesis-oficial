from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .equivalencia_replicadas_service import EquivalenciaReplicadasService
from .equivalencia_replicadas_model import EquivalenciaReplicadas, UpdateEquivalenciaReplicadas

@Controller("equivalencia_replicadas")
class EquivalenciaReplicadasController:

    def __init__(self, equivalencia_replicadas_service: EquivalenciaReplicadasService):
        self.equivalencia_replicadas_service = equivalencia_replicadas_service

    @Get("/")
    async def get_equivalencia_replicadas(self, session: AsyncSession = Depends(config.get_db)):
        return await self.equivalencia_replicadas_service.get_equivalencia_replicadas(session)

    @Get("/{equivalencia_replicada_id}")
    async def get_equivalencia_replicada_by_id(self, equivalencia_replicada_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.equivalencia_replicadas_service.get_equivalencia_replicada_by_id(equivalencia_replicada_id, session)

    @Post("/")
    async def add_equivalencia_replicada(self, equivalencia_replicada: EquivalenciaReplicadas, session: AsyncSession = Depends(config.get_db)):
        return await self.equivalencia_replicadas_service.add_equivalencia_replicada(equivalencia_replicada, session)

    @Put("/{equivalencia_replicada_id}")
    async def update_equivalencia_replicada(self, equivalencia_replicada_id: int, equivalencia_replicada_update: UpdateEquivalenciaReplicadas, session: AsyncSession = Depends(config.get_db)):
        return await self.equivalencia_replicadas_service.update_equivalencia_replicada(equivalencia_replicada_id, equivalencia_replicada_update, session)

    @Delete("/{equivalencia_replicada_id}")
    async def delete_equivalencia_replicada(self, equivalencia_replicada_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.equivalencia_replicadas_service.delete_equivalencia_replicada(equivalencia_replicada_id, session)
