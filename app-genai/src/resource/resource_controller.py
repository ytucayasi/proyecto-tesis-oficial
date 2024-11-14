from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .resource_service import ResourceService
from .resource_model import Resource, UpdateResource

@Controller("resources")
class ResourceController:
    def __init__(self, resource_service: ResourceService):
        self.resource_service = resource_service

    @Get("/")
    async def get_resources(self, session: AsyncSession = Depends(config.get_db)):
        return await self.resource_service.get_resources(session)

    @Get("/{resource_id}")
    async def get_resource(self, resource_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.resource_service.get_resource(resource_id, session)

    @Post("/")
    async def create_resource(self, resource: Resource, session: AsyncSession = Depends(config.get_db)):
        return await self.resource_service.create_resource(resource, session)

    @Put("/{resource_id}")
    async def update_resource(self, resource_id: int, resource: UpdateResource, session: AsyncSession = Depends(config.get_db)):
        return await self.resource_service.update_resource(resource_id, resource, session)

    @Delete("/{resource_id}")
    async def delete_resource(self, resource_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.resource_service.delete_resource(resource_id, session)