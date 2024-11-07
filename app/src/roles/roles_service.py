from .roles_model import Roles, UpdateRoles
from .roles_entity import Roles as RolesEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class RolesService:

    @async_db_request_handler
    async def add_rol(self, rol: Roles, session: AsyncSession):
        new_rol = RolesEntity(**rol.dict())
        session.add(new_rol)
        await session.commit()
        return {"rol_id": new_rol.rol_id}

    @async_db_request_handler
    async def get_roles(self, session: AsyncSession):
        query = select(RolesEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_rol_by_id(self, rol_id: int, session: AsyncSession):
        query = select(RolesEntity).where(RolesEntity.rol_id == rol_id)
        result = await session.execute(query)
        rol = result.scalar_one_or_none()
        if rol is None:
            raise HTTPException(status_code=404, detail=f"Role with id {rol_id} not found")
        return rol

    @async_db_request_handler
    async def update_rol(self, rol_id: int, rol_update: UpdateRoles, session: AsyncSession):
        rol = await self.get_rol_by_id(rol_id, session)
        update_data = rol_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(RolesEntity).where(RolesEntity.rol_id == rol_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_rol_by_id(rol_id, session)

    @async_db_request_handler
    async def delete_rol(self, rol_id: int, session: AsyncSession):
        await self.get_rol_by_id(rol_id, session)
        query = delete(RolesEntity).where(RolesEntity.rol_id == rol_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Role with id {rol_id} has been deleted"}
