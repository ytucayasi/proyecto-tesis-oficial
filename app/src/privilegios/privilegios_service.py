from .privilegios_model import Privilegios, UpdatePrivilegios
from .privilegios_entity import Privilegios as PrivilegiosEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class PrivilegiosService:

    @async_db_request_handler
    async def add_privilegio(self, privilegio: Privilegios, session: AsyncSession):
        new_privilegio = PrivilegiosEntity(**privilegio.dict())
        session.add(new_privilegio)
        await session.commit()
        return {"privilegio_id": new_privilegio.privilegio_id}

    @async_db_request_handler
    async def get_privilegios(self, session: AsyncSession):
        query = select(PrivilegiosEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_privilegio_by_id(self, privilegio_id: int, session: AsyncSession):
        query = select(PrivilegiosEntity).where(PrivilegiosEntity.privilegio_id == privilegio_id)
        result = await session.execute(query)
        privilegio = result.scalar_one_or_none()
        if privilegio is None:
            raise HTTPException(status_code=404, detail=f"Privilegio with id {privilegio_id} not found")
        return privilegio

    @async_db_request_handler
    async def update_privilegio(self, privilegio_id: int, privilegio_update: UpdatePrivilegios, session: AsyncSession):
        privilegio = await self.get_privilegio_by_id(privilegio_id, session)
        update_data = privilegio_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(PrivilegiosEntity).where(PrivilegiosEntity.privilegio_id == privilegio_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_privilegio_by_id(privilegio_id, session)

    @async_db_request_handler
    async def delete_privilegio(self, privilegio_id: int, session: AsyncSession):
        await self.get_privilegio_by_id(privilegio_id, session)
        query = delete(PrivilegiosEntity).where(PrivilegiosEntity.privilegio_id == privilegio_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Privilegio with id {privilegio_id} has been deleted"}
