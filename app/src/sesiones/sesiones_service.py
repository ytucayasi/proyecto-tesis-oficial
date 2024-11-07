from .sesiones_model import Sesiones, UpdateSesiones
from .sesiones_entity import Sesiones as SesionesEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class SesionesService:

    @async_db_request_handler
    async def add_sesion(self, sesion: Sesiones, session: AsyncSession):
        new_sesion = SesionesEntity(**sesion.dict())
        session.add(new_sesion)
        await session.commit()
        return {"sesion_id": new_sesion.sesion_id}

    @async_db_request_handler
    async def get_sesiones(self, session: AsyncSession):
        query = select(SesionesEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_sesion_by_id(self, sesion_id: int, session: AsyncSession):
        query = select(SesionesEntity).where(SesionesEntity.sesion_id == sesion_id)
        result = await session.execute(query)
        sesion = result.scalar_one_or_none()
        if sesion is None:
            raise HTTPException(status_code=404, detail=f"Sesion with id {sesion_id} not found")
        return sesion

    @async_db_request_handler
    async def update_sesion(self, sesion_id: int, sesion_update: UpdateSesiones, session: AsyncSession):
        sesion = await self.get_sesion_by_id(sesion_id, session)
        update_data = sesion_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(SesionesEntity).where(SesionesEntity.sesion_id == sesion_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_sesion_by_id(sesion_id, session)

    @async_db_request_handler
    async def delete_sesion(self, sesion_id: int, session: AsyncSession):
        await self.get_sesion_by_id(sesion_id, session)
        query = delete(SesionesEntity).where(SesionesEntity.sesion_id == sesion_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Sesion with id {sesion_id} has been deleted"}
