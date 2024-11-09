from .usuarios_model import Usuarios, UpdateUsuarios
from .usuarios_entity import Usuarios as UsuariosEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class UsuariosService:

    @async_db_request_handler
    async def add_usuario(self, usuario: Usuarios, session: AsyncSession):
        new_usuario = UsuariosEntity(**usuario.dict())
        session.add(new_usuario)
        await session.commit()
        return new_usuario.correo_electronico

    @async_db_request_handler
    async def get_usuarios(self, session: AsyncSession):
        query = select(UsuariosEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_usuario_by_id(self, usuario_id: int, session: AsyncSession):
        query = select(UsuariosEntity).where(UsuariosEntity.usuario_id == usuario_id)
        result = await session.execute(query)
        usuario = result.scalar_one_or_none()
        if usuario is None:
            raise HTTPException(status_code=404, detail=f"Usuario with id {usuario_id} not found")
        return usuario

    @async_db_request_handler
    async def update_usuario(self, usuario_id: int, usuario_update: UpdateUsuarios, session: AsyncSession):
        usuario = await self.get_usuario_by_id(usuario_id, session)
        update_data = usuario_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(UsuariosEntity).where(UsuariosEntity.usuario_id == usuario_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_usuario_by_id(usuario_id, session)

    @async_db_request_handler
    async def delete_usuario(self, usuario_id: int, session: AsyncSession):
        await self.get_usuario_by_id(usuario_id, session)
        query = delete(UsuariosEntity).where(UsuariosEntity.usuario_id == usuario_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Usuario with id {usuario_id} has been deleted"}
