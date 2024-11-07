from .curso_equivalencias_model import CursoEquivalencias, UpdateCursoEquivalencias
from .curso_equivalencias_entity import CursoEquivalencias as CursoEquivalenciasEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class CursoEquivalenciasService:

    @async_db_request_handler
    async def add_curso_equivalencia(self, curso_equivalencia: CursoEquivalencias, session: AsyncSession):
        new_curso_equivalencia = CursoEquivalenciasEntity(**curso_equivalencia.dict())
        session.add(new_curso_equivalencia)
        await session.commit()
        return {"curso_equivalencia_id": new_curso_equivalencia.curso_equivalencia_id}

    @async_db_request_handler
    async def get_curso_equivalencias(self, session: AsyncSession):
        query = select(CursoEquivalenciasEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_curso_equivalencia_by_id(self, curso_equivalencia_id: int, session: AsyncSession):
        query = select(CursoEquivalenciasEntity).where(CursoEquivalenciasEntity.curso_equivalencia_id == curso_equivalencia_id)
        result = await session.execute(query)
        curso_equivalencia = result.scalar_one_or_none()
        if curso_equivalencia is None:
            raise HTTPException(status_code=404, detail=f"CursoEquivalencia with id {curso_equivalencia_id} not found")
        return curso_equivalencia

    @async_db_request_handler
    async def update_curso_equivalencia(self, curso_equivalencia_id: int, curso_equivalencia_update: UpdateCursoEquivalencias, session: AsyncSession):
        curso_equivalencia = await self.get_curso_equivalencia_by_id(curso_equivalencia_id, session)
        update_data = curso_equivalencia_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(CursoEquivalenciasEntity).where(CursoEquivalenciasEntity.curso_equivalencia_id == curso_equivalencia_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_curso_equivalencia_by_id(curso_equivalencia_id, session)

    @async_db_request_handler
    async def delete_curso_equivalencia(self, curso_equivalencia_id: int, session: AsyncSession):
        await self.get_curso_equivalencia_by_id(curso_equivalencia_id, session)
        query = delete(CursoEquivalenciasEntity).where(CursoEquivalenciasEntity.curso_equivalencia_id == curso_equivalencia_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"CursoEquivalencia with id {curso_equivalencia_id} has been deleted"}
