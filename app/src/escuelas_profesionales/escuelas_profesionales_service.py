from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from .escuelas_profesionales_model import EscuelaProfesional, UpdateEscuelaProfesional
from .escuelas_profesionales_entity import EscuelaProfesional as EscuelaProfesionalEntity

@Injectable
class EscuelasProfesionalesService:
    @async_db_request_handler
    async def create_escuela_profesional(self, escuela_profesional: EscuelaProfesional, session: AsyncSession):
        new_escuela = EscuelaProfesionalEntity(**escuela_profesional.dict())
        session.add(new_escuela)
        await session.commit()
        await session.refresh(new_escuela)
        return new_escuela

    @async_db_request_handler
    async def get_escuelas_profesionales(self, session: AsyncSession):
        query = select(EscuelaProfesionalEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_escuela_profesional_by_id(self, escuela_profesional_id: int, session: AsyncSession):
        query = select(EscuelaProfesionalEntity).where(EscuelaProfesionalEntity.escuela_profesional_id == escuela_profesional_id)
        result = await session.execute(query)
        escuela_profesional = result.scalar_one_or_none()
        
        if escuela_profesional is None:
            raise HTTPException(status_code=404, detail=f"EscuelaProfesional with id {escuela_profesional_id} not found")
            
        return escuela_profesional

    @async_db_request_handler
    async def update_escuela_profesional(self, escuela_profesional_id: int, escuela_profesional_update: UpdateEscuelaProfesional, session: AsyncSession):
        await self.get_escuela_profesional_by_id(escuela_profesional_id, session)
        update_data = escuela_profesional_update.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        query = update(EscuelaProfesionalEntity).where(EscuelaProfesionalEntity.escuela_profesional_id == escuela_profesional_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        
        return await self.get_escuela_profesional_by_id(escuela_profesional_id, session)

    @async_db_request_handler
    async def delete_escuela_profesional(self, escuela_profesional_id: int, session: AsyncSession):
        await self.get_escuela_profesional_by_id(escuela_profesional_id, session)
        query = delete(EscuelaProfesionalEntity).where(EscuelaProfesionalEntity.escuela_profesional_id == escuela_profesional_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"EscuelaProfesional with id {escuela_profesional_id} has been deleted"}
