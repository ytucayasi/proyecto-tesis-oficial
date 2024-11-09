from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from .secuencia_aprendizaje_entity import SecuenciaAprendizajeEntity
from .secuencia_aprendizaje_model import SecuenciaAprendizaje, UpdateSecuenciaAprendizaje

@Injectable()
class SecuenciaAprendizajeService:
    async def get_secuencias(self, session: AsyncSession) -> List[SecuenciaAprendizajeEntity]:
        query = select(SecuenciaAprendizajeEntity)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_secuencias_by_sesion(
        self,
        sesion_id: int,
        session: AsyncSession
    ) -> List[SecuenciaAprendizajeEntity]:
        query = select(SecuenciaAprendizajeEntity).where(
            SecuenciaAprendizajeEntity.sesion_aprendizaje_id == sesion_id
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_secuencia_by_id(
        self, 
        secuencia_id: int, 
        session: AsyncSession
    ) -> SecuenciaAprendizajeEntity:
        query = select(SecuenciaAprendizajeEntity).where(
            SecuenciaAprendizajeEntity.secuencia_aprendizaje_id == secuencia_id
        )
        result = await session.execute(query)
        secuencia = result.scalar_one_or_none()
        
        if not secuencia:
            raise HTTPException(
                status_code=404, 
                detail="Secuencia de aprendizaje no encontrada"
            )
        return secuencia

    async def create_secuencia(
        self, 
        secuencia: SecuenciaAprendizaje, 
        session: AsyncSession
    ) -> SecuenciaAprendizajeEntity:
        new_secuencia = SecuenciaAprendizajeEntity(
            sesion_aprendizaje_id=secuencia.sesion_aprendizaje_id,
            tipo_secuencia_id=secuencia.tipo_secuencia_id,
            link_recurso=secuencia.link_recurso,
            link_rubrica=secuencia.link_rubrica,
            estado_recursos=secuencia.estado_recursos
        )
        session.add(new_secuencia)
        await session.commit()
        await session.refresh(new_secuencia)
        return new_secuencia

    async def update_secuencia(
        self, 
        secuencia_id: int, 
        secuencia: UpdateSecuenciaAprendizaje, 
        session: AsyncSession
    ) -> SecuenciaAprendizajeEntity:
        db_secuencia = await self.get_secuencia_by_id(secuencia_id, session)
        
        update_data = secuencia.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_secuencia, key, value)

        await session.commit()
        await session.refresh(db_secuencia)
        return db_secuencia

    async def delete_secuencia(
        self, 
        secuencia_id: int, 
        session: AsyncSession
    ) -> bool:
        secuencia = await self.get_secuencia_by_id(secuencia_id, session)
        await session.delete(secuencia)
        await session.commit()
        return True