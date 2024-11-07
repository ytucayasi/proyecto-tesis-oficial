from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from .historial_recurso_entity import HistorialRecursoEntity
from .historial_recurso_model import HistorialRecurso, UpdateHistorialRecurso

@Injectable()
class HistorialRecursoService:
    async def get_historiales(self, session: AsyncSession) -> List[HistorialRecursoEntity]:
        query = select(HistorialRecursoEntity)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_generacion(
        self,
        generacion_id: int,
        session: AsyncSession
    ) -> List[HistorialRecursoEntity]:
        query = select(HistorialRecursoEntity).where(
            HistorialRecursoEntity.generacion_recurso_id == generacion_id
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_evaluacion(
        self,
        evaluacion_id: int,
        session: AsyncSession
    ) -> List[HistorialRecursoEntity]:
        query = select(HistorialRecursoEntity).where(
            HistorialRecursoEntity.evaluacion_id == evaluacion_id
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_id(
        self, 
        historial_id: int, 
        session: AsyncSession
    ) -> HistorialRecursoEntity:
        query = select(HistorialRecursoEntity).where(
            HistorialRecursoEntity.historial_recurso_id == historial_id
        )
        result = await session.execute(query)
        historial = result.scalar_one_or_none()
        
        if not historial:
            raise HTTPException(
                status_code=404, 
                detail="Historial de recurso no encontrado"
            )
        return historial

    async def create_historial(
        self, 
        historial: HistorialRecurso, 
        session: AsyncSession
    ) -> HistorialRecursoEntity:
        new_historial = HistorialRecursoEntity(
            generacion_recurso_id=historial.generacion_recurso_id,
            evaluacion_id=historial.evaluacion_id,
            fecha_generacion=historial.fecha_generacion or datetime.utcnow(),
            estado_recurso=historial.estado_recurso
        )
        session.add(new_historial)
        await session.commit()
        await session.refresh(new_historial)
        return new_historial

    async def update_historial(
        self, 
        historial_id: int, 
        historial: UpdateHistorialRecurso, 
        session: AsyncSession
    ) -> HistorialRecursoEntity:
        db_historial = await self.get_by_id(historial_id, session)
        
        update_data = historial.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_historial, key, value)

        await session.commit()
        await session.refresh(db_historial)
        return db_historial

    async def delete_historial(
        self, 
        historial_id: int, 
        session: AsyncSession
    ) -> bool:
        historial = await self.get_by_id(historial_id, session)
        await session.delete(historial)
        await session.commit()
        return True