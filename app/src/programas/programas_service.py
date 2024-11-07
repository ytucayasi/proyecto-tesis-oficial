from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from .programas_model import Programa, UpdatePrograma
from .programas_entity import Programa as ProgramaEntity

@Injectable
class ProgramasService:
    @async_db_request_handler
    async def create_programa(self, programa: Programa, session: AsyncSession):
        new_programa = ProgramaEntity(**programa.dict())
        session.add(new_programa)
        await session.commit()
        await session.refresh(new_programa)
        return new_programa

    @async_db_request_handler
    async def get_programas(self, session: AsyncSession):
        query = select(ProgramaEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_programa_by_id(self, programa_id: int, session: AsyncSession):
        query = select(ProgramaEntity).where(ProgramaEntity.programa_id == programa_id)
        result = await session.execute(query)
        programa = result.scalar_one_or_none()

        if programa is None:
            raise HTTPException(status_code=404, detail=f"Programa with id {programa_id} not found")

        return programa

    @async_db_request_handler
    async def update_programa(self, programa_id: int, programa_update: UpdatePrograma, session: AsyncSession):
        await self.get_programa_by_id(programa_id, session)
        update_data = programa_update.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        query = update(ProgramaEntity).where(ProgramaEntity.programa_id == programa_id).values(**update_data)
        await session.execute(query)
        await session.commit()

        return await self.get_programa_by_id(programa_id, session)

    @async_db_request_handler
    async def delete_programa(self, programa_id: int, session: AsyncSession):
        await self.get_programa_by_id(programa_id, session)
        query = delete(ProgramaEntity).where(ProgramaEntity.programa_id == programa_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Programa with id {programa_id} has been deleted"}
