from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from .niveles_model import Nivel, UpdateNivel
from .niveles_entity import Nivel as NivelEntity

@Injectable
class NivelesService:
    @async_db_request_handler
    async def create_nivel(self, nivel: Nivel, session: AsyncSession):
        new_nivel = NivelEntity(**nivel.dict())
        session.add(new_nivel)
        await session.commit()
        await session.refresh(new_nivel)
        return new_nivel

    @async_db_request_handler
    async def get_niveles(self, session: AsyncSession):
        query = select(NivelEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_nivel_by_id(self, nivel_id: int, session: AsyncSession):
        query = select(NivelEntity).where(NivelEntity.nivel_id == nivel_id)
        result = await session.execute(query)
        nivel = result.scalar_one_or_none()
        
        if nivel is None:
            raise HTTPException(status_code=404, detail=f"Nivel with id {nivel_id} not found")
            
        return nivel

    @async_db_request_handler
    async def update_nivel(self, nivel_id: int, nivel_update: UpdateNivel, session: AsyncSession):
        await self.get_nivel_by_id(nivel_id, session)
        update_data = nivel_update.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        query = update(NivelEntity).where(NivelEntity.nivel_id == nivel_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        
        return await self.get_nivel_by_id(nivel_id, session)

    @async_db_request_handler
    async def delete_nivel(self, nivel_id: int, session: AsyncSession):
        await self.get_nivel_by_id(nivel_id, session)
        query = delete(NivelEntity).where(NivelEntity.nivel_id == nivel_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Nivel with id {nivel_id} has been deleted"}
