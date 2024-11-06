from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .users_service import UsersService
from .users_model import Users, UpdateUser

@Controller("users")
class UsersController:

    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    @Get("/")
    async def get_users(self, session: AsyncSession = Depends(config.get_db)):
        return await self.users_service.get_users(session)
    
    @Get("/{user_id}")
    async def get_user_by_id(self, user_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.users_service.get_user_by_id(user_id, session)

    @Get("/name/{name}")
    async def get_user_by_name(self, name: str, session: AsyncSession = Depends(config.get_db)):
        return await self.users_service.get_user_by_name(name, session)

    @Post("/")
    async def add_users(self, users: Users, session: AsyncSession = Depends(config.get_db)):
        return await self.users_service.add_users(users, session)
    
    @Put("/{user_id}")
    async def update_user(self, user_id: int, user_update: UpdateUser, session: AsyncSession = Depends(config.get_db)):
        return await self.users_service.update_user(user_id, user_update, session)

    @Delete("/{user_id}")
    async def delete_user(self, user_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.users_service.delete_user(user_id, session)
  