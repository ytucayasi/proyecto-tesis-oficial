from .rol_privilegios_model import RolPrivilegios, UpdateRolPrivilegios
from .rol_privilegios_entity import RolPrivilegios as RolPrivilegiosEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class RolPrivilegiosService:

    @async_db_request_handler
    async def add_rol_privilegio(self, rol_privilegio: RolPrivilegios, session: AsyncSession):
        new_rol_privilegio = RolPrivilegiosEntity(**rol_privilegio.dict())
        session.add(new_rol_privilegio)
        await session.commit()
        return {"rol_privilegio_id": new_rol_privilegio.rol_privilegio_id}

    @async_db_request_handler
    async def get_rol_privilegios(self, session: AsyncSession):
        query = select(RolPrivilegiosEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_rol_privilegio_by_id(self, rol_privilegio_id: int, session: AsyncSession):
        query = select(RolPrivilegiosEntity).where(RolPrivilegiosEntity.rol_privilegio_id == rol_privilegio_id)
        result = await session.execute(query)
        rol_privilegio = result.scalar_one_or_none()
        if rol_privilegio is None:
            raise HTTPException(status_code=404, detail=f"RolPrivilegio with id {rol_privilegio_id} not found")
        return rol_privilegio

    @async_db_request_handler
    async def update_rol_privilegio(self, rol_privilegio_id: int, rol_privilegio_update: UpdateRolPrivilegios, session: AsyncSession):
        rol_privilegio = await self.get_rol_privilegio_by_id(rol_privilegio_id, session)
        update_data = rol_privilegio_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(RolPrivilegiosEntity).where(RolPrivilegiosEntity.rol_privilegio_id == rol_privilegio_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_rol_privilegio_by_id(rol_privilegio_id, session)

    @async_db_request_handler
    async def delete_rol_privilegio(self, rol_privilegio_id: int, session: AsyncSession):
        await self.get_rol_privilegio_by_id(rol_privilegio_id, session)
        query = delete(RolPrivilegiosEntity).where(RolPrivilegiosEntity.rol_privilegio_id == rol_privilegio_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"RolPrivilegio with id {rol_privilegio_id} has been deleted"}
