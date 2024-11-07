from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from .planes_academicos_model import PlanAcademico, UpdatePlanAcademico
from .planes_academicos_entity import PlanAcademico as PlanAcademicoEntity

@Injectable
class PlanesAcademicosService:
    @async_db_request_handler
    async def create_plan_academico(self, plan_academico: PlanAcademico, session: AsyncSession):
        new_plan = PlanAcademicoEntity(**plan_academico.dict())
        session.add(new_plan)
        await session.commit()
        await session.refresh(new_plan)
        return new_plan

    @async_db_request_handler
    async def get_planes_academicos(self, session: AsyncSession):
        query = select(PlanAcademicoEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_plan_academico_by_id(self, plan_academico_id: int, session: AsyncSession):
        query = select(PlanAcademicoEntity).where(PlanAcademicoEntity.plan_academico_id == plan_academico_id)
        result = await session.execute(query)
        plan_academico = result.scalar_one_or_none()

        if plan_academico is None:
            raise HTTPException(status_code=404, detail=f"PlanAcademico with id {plan_academico_id} not found")

        return plan_academico

    @async_db_request_handler
    async def update_plan_academico(self, plan_academico_id: int, plan_academico_update: UpdatePlanAcademico, session: AsyncSession):
        await self.get_plan_academico_by_id(plan_academico_id, session)
        update_data = plan_academico_update.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        query = update(PlanAcademicoEntity).where(PlanAcademicoEntity.plan_academico_id == plan_academico_id).values(**update_data)
        await session.execute(query)
        await session.commit()

        return await self.get_plan_academico_by_id(plan_academico_id, session)

    @async_db_request_handler
    async def delete_plan_academico(self, plan_academico_id: int, session: AsyncSession):
        await self.get_plan_academico_by_id(plan_academico_id, session)
        query = delete(PlanAcademicoEntity).where(PlanAcademicoEntity.plan_academico_id == plan_academico_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"PlanAcademico with id {plan_academico_id} has been deleted"}
