from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from .unidad_entity import UnidadEntity
from .unidad_model import Unidad, UpdateUnidad

@Injectable()
class UnidadService:
    async def get_unidades(self, session: AsyncSession) -> List[UnidadEntity]:
        query = select(UnidadEntity)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_unidades_by_curso(
        self,
        curso_id: int,
        session: AsyncSession
    ) -> List[UnidadEntity]:
        query = select(UnidadEntity).where(UnidadEntity.curso_id == curso_id)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_unidad_by_id(
        self, 
        unidad_id: int, 
        session: AsyncSession
    ) -> UnidadEntity:
        query = select(UnidadEntity).where(
            UnidadEntity.unidad_id == unidad_id
        )
        result = await session.execute(query)
        unidad = result.scalar_one_or_none()
        
        if not unidad:
            raise HTTPException(
                status_code=404, 
                detail="Unidad no encontrada"
            )
        return unidad

    async def create_unidad(
        self, 
        unidad: Unidad, 
        session: AsyncSession
    ) -> UnidadEntity:
        new_unidad = UnidadEntity(
            curso_id=unidad.curso_id,
            nombre=unidad.nombre,
            resultado_aprendizaje=unidad.resultado_aprendizaje,
            descripcion=unidad.descripcion
        )
        session.add(new_unidad)
        await session.commit()
        await session.refresh(new_unidad)
        return new_unidad

    async def update_unidad(
        self, 
        unidad_id: int, 
        unidad: UpdateUnidad, 
        session: AsyncSession
    ) -> UnidadEntity:
        db_unidad = await self.get_unidad_by_id(unidad_id, session)
        
        update_data = unidad.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_unidad, key, value)

        await session.commit()
        await session.refresh(db_unidad)
        return db_unidad

    async def delete_unidad(
        self, 
        unidad_id: int, 
        session: AsyncSession
    ) -> bool:
        unidad = await self.get_unidad_by_id(unidad_id, session)
        await session.delete(unidad)
        await session.commit()
        return True