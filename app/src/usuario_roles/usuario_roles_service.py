from .usuario_roles_model import UsuarioRoles, UpdateUsuarioRoles
from .usuario_roles_entity import UsuarioRoles as UsuarioRolesEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class UsuarioRolesService:

    @async_db_request_handler
    async def add_usuario_rol(self, usuario_rol: UsuarioRoles, session: AsyncSession):
        new_usuario_rol = UsuarioRolesEntity(**usuario_rol.dict())
        session.add(new_usuario_rol)
        await session.commit()
        return {"usuario_rol_id": new_usuario_rol.usuario_rol_id}

    @async_db_request_handler
    async def get_usuario_roles(self, session: AsyncSession):
        query = select(UsuarioRolesEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_usuario_rol_by_id(self, usuario_rol_id: int, session: AsyncSession):
        query = select(UsuarioRolesEntity).where(UsuarioRolesEntity.usuario_rol_id == usuario_rol_id)
        result = await session.execute(query)
        usuario_rol = result.scalar_one_or_none()
        if usuario_rol is None:
            raise HTTPException(status_code=404, detail=f"UsuarioRol with id {usuario_rol_id} not found")
        return usuario_rol

    @async_db_request_handler
    async def update_usuario_rol(self, usuario_rol_id: int, usuario_rol_update: UpdateUsuarioRoles, session: AsyncSession):
        usuario_rol = await self.get_usuario_rol_by_id(usuario_rol_id, session)
        update_data = usuario_rol_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(UsuarioRolesEntity).where(UsuarioRolesEntity.usuario_rol_id == usuario_rol_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_usuario_rol_by_id(usuario_rol_id, session)

    @async_db_request_handler
    async def delete_usuario_rol(self, usuario_rol_id: int, session: AsyncSession):
        await self.get_usuario_rol_by_id(usuario_rol_id, session)
        query = delete(UsuarioRolesEntity).where(UsuarioRolesEntity.usuario_rol_id == usuario_rol_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"UsuarioRol with id {usuario_rol_id} has been deleted"}
