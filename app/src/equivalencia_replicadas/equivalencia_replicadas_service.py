from .equivalencia_replicadas_model import EquivalenciaReplicadas, UpdateEquivalenciaReplicadas
from .equivalencia_replicadas_entity import EquivalenciaReplicadas as EquivalenciaReplicadasEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class EquivalenciaReplicadasService:

    @async_db_request_handler
    async def add_equivalencia_replicada(self, equivalencia_replicada: EquivalenciaReplicadas, session: AsyncSession):
        new_equivalencia_replicada = EquivalenciaReplicadasEntity(**equivalencia_replicada.dict())
        session.add(new_equivalencia_replicada)
        await session.commit()
        return {"equivalencia_replicada_id": new_equivalencia_replicada.equivalencia_replicada_id}

    @async_db_request_handler
    async def get_equivalencia_replicadas(self, session: AsyncSession):
        query = select(EquivalenciaReplicadasEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_equivalencia_replicada_by_id(self, equivalencia_replicada_id: int, session: AsyncSession):
        query = select(EquivalenciaReplicadasEntity).where(EquivalenciaReplicadasEntity.equivalencia_replicada_id == equivalencia_replicada_id)
        result = await session.execute(query)
        equivalencia_replicada = result.scalar_one_or_none()
        if equivalencia_replicada is None:
            raise HTTPException(status_code=404, detail=f"EquivalenciaReplicada with id {equivalencia_replicada_id} not found")
        return equivalencia_replicada

    @async_db_request_handler
    async def update_equivalencia_replicada(self, equivalencia_replicada_id: int, equivalencia_replicada_update: UpdateEquivalenciaReplicadas, session: AsyncSession):
        equivalencia_replicada = await self.get_equivalencia_replicada_by_id(equivalencia_replicada_id, session)
        update_data = equivalencia_replicada_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(EquivalenciaReplicadasEntity).where(EquivalenciaReplicadasEntity.equivalencia_replicada_id == equivalencia_replicada_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_equivalencia_replicada_by_id(equivalencia_replicada_id, session)

    @async_db_request_handler
    async def delete_equivalencia_replicada(self, equivalencia_replicada_id: int, session: AsyncSession):
        await self.get_equivalencia_replicada_by_id(equivalencia_replicada_id, session)
        query = delete(EquivalenciaReplicadasEntity).where(EquivalenciaReplicadasEntity.equivalencia_replicada_id == equivalencia_replicada_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"EquivalenciaReplicada with id {equivalencia_replicada_id} has been deleted"}
