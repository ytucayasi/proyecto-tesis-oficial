from .evaluaciones_model import Evaluaciones, UpdateEvaluaciones
from .evaluaciones_entity import Evaluaciones as EvaluacionesEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

@Injectable
class EvaluacionesService:

    @async_db_request_handler
    async def add_evaluacion(self, evaluacion: Evaluaciones, session: AsyncSession):
        new_evaluacion = EvaluacionesEntity(**evaluacion.dict())
        session.add(new_evaluacion)
        await session.commit()
        return {"evaluar_id": new_evaluacion.evaluar_id}

    @async_db_request_handler
    async def get_evaluaciones(self, session: AsyncSession):
        query = select(EvaluacionesEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_evaluacion_by_id(self, evaluar_id: int, session: AsyncSession):
        query = select(EvaluacionesEntity).where(EvaluacionesEntity.evaluar_id == evaluar_id)
        result = await session.execute(query)
        evaluacion = result.scalar_one_or_none()
        if evaluacion is None:
            raise HTTPException(status_code=404, detail=f"Evaluacion with id {evaluar_id} not found")
        return evaluacion

    @async_db_request_handler
    async def update_evaluacion(self, evaluar_id: int, evaluacion_update: UpdateEvaluaciones, session: AsyncSession):
        evaluacion = await self.get_evaluacion_by_id(evaluar_id, session)
        update_data = evaluacion_update.dict(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        query = update(EvaluacionesEntity).where(EvaluacionesEntity.evaluar_id == evaluar_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await self.get_evaluacion_by_id(evaluar_id, session)

    @async_db_request_handler
    async def delete_evaluacion(self, evaluar_id: int, session: AsyncSession):
        await self.get_evaluacion_by_id(evaluar_id, session)
        query = delete(EvaluacionesEntity).where(EvaluacionesEntity.evaluar_id == evaluar_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Evaluacion with id {evaluar_id} has been deleted"}
