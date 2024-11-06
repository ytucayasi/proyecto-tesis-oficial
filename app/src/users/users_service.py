from .users_model import Users, UpdateUser
from .users_entity import Users as UsersEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class UsersService:

    @async_db_request_handler
    async def add_users(self, users: Users, session: AsyncSession):
        new_users = UsersEntity(**users.dict())
        session.add(new_users)
        await session.commit()
        return new_users.name

    @async_db_request_handler
    async def get_users(self, session: AsyncSession):
        query = select(UsersEntity)
        result = await session.execute(query)
        return result.scalars().all()
    
    @async_db_request_handler
    async def get_user_by_id(self, user_id: int, session: AsyncSession):
        query = select(UsersEntity).where(UsersEntity.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        return user

    @async_db_request_handler
    async def get_user_by_name(self, name: str, session: AsyncSession):
        query = select(UsersEntity).where(UsersEntity.name == name)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail=f"User with name {name} not found")
        return user

    @async_db_request_handler
    async def update_user(self, user_id: int, user_update: UpdateUser, session: AsyncSession):
        user = await self.get_user_by_id(user_id, session)
        update_data = user_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(UsersEntity).where(UsersEntity.id == user_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_user_by_id(user_id, session)

    @async_db_request_handler
    async def delete_user(self, user_id: int, session: AsyncSession):
        await self.get_user_by_id(user_id, session)
        query = delete(UsersEntity).where(UsersEntity.id == user_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"User with id {user_id} has been deleted"}