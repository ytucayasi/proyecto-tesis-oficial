from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from .ciclos_model import Ciclo, UpdateCiclo
from .ciclos_entity import Ciclo as CicloEntity

@Injectable
class CiclosService:
    @async_db_request_handler
    async def create_ciclo(self, ciclo: Ciclo, session: AsyncSession):
        new_ciclo = CicloEntity(**ciclo.dict())
        session.add(new_ciclo)
        await session.commit()
        await session.refresh(new_ciclo)
        return new_ciclo

    @async_db_request_handler
    async def get_ciclos(self, session: AsyncSession):
        query = select(CicloEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_ciclo_by_id(self, ciclo_id: int, session: AsyncSession):
        query = select(CicloEntity).where(CicloEntity.ciclo_id == ciclo_id)
        result = await session.execute(query)
        ciclo = result.scalar_one_or_none()

        if ciclo is None:
            raise HTTPException(status_code=404, detail=f"Ciclo with id {ciclo_id} not found")

        return ciclo

    @async_db_request_handler
    async def update_ciclo(self, ciclo_id: int, ciclo_update: UpdateCiclo, session: AsyncSession):
        await self.get_ciclo_by_id(ciclo_id, session)
        update_data = ciclo_update.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        query = update(CicloEntity).where(CicloEntity.ciclo_id == ciclo_id).values(**update_data)
        await session.execute(query)
        await session.commit()

        return await self.get_ciclo_by_id(ciclo_id, session)

    @async_db_request_handler
    async def delete_ciclo(self, ciclo_id: int, session: AsyncSession):
        await self.get_ciclo_by_id(ciclo_id, session)
        query = delete(CicloEntity).where(CicloEntity.ciclo_id == ciclo_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Ciclo with id {ciclo_id} has been deleted"}
