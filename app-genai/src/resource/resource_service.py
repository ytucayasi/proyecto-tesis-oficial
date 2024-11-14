from nest.core import Injectable
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .resource_model import Resource, UpdateResource
from .resource_entity import ResourceEntity

@Injectable()
class ResourceService:
    async def get_resources(self, session: AsyncSession):
        query = select(ResourceEntity)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_resource(self, resource_id: int, session: AsyncSession):
        query = select(ResourceEntity).where(ResourceEntity.resource_id == resource_id)
        result = await session.execute(query)
        resource = result.scalar_one_or_none()
        
        if not resource:
            raise HTTPException(status_code=404, detail=f"Resource {resource_id} not found")
            
        return resource

    async def create_resource(self, resource: Resource, session: AsyncSession):
        db_resource = ResourceEntity(**resource.dict())
        session.add(db_resource)
        await session.commit()
        await session.refresh(db_resource)
        return db_resource

    async def update_resource(self, resource_id: int, resource: UpdateResource, session: AsyncSession):
        db_resource = await self.get_resource(resource_id, session)
        update_data = resource.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(db_resource, key, value)
            
        await session.commit()
        await session.refresh(db_resource)
        return db_resource

    async def delete_resource(self, resource_id: int, session: AsyncSession):
        db_resource = await self.get_resource(resource_id, session)
        await session.delete(db_resource)
        await session.commit()
        return {"message": f"Resource {resource_id} deleted"}