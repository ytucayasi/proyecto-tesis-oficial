from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from .sesion_aprendizaje_entity import SesionAprendizajeEntity
from .sesion_aprendizaje_model import SesionAprendizaje, UpdateSesionAprendizaje

@Injectable()
class SesionAprendizajeService:
    async def get_sesiones(self, session: AsyncSession) -> List[SesionAprendizajeEntity]:
        query = select(SesionAprendizajeEntity)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_sesiones_by_unidad(
        self,
        unidad_id: int,
        session: AsyncSession
    ) -> List[SesionAprendizajeEntity]:
        query = select(SesionAprendizajeEntity).where(
            SesionAprendizajeEntity.unidad_id == unidad_id
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_sesion_by_id(
        self, 
        sesion_id: int, 
        session: AsyncSession
    ) -> SesionAprendizajeEntity:
        query = select(SesionAprendizajeEntity).where(
            SesionAprendizajeEntity.sesion_aprendizaje_id == sesion_id
        )
        result = await session.execute(query)
        sesion = result.scalar_one_or_none()
        
        if not sesion:
            raise HTTPException(
                status_code=404, 
                detail="Sesión de aprendizaje no encontrada"
            )
        return sesion

    async def create_sesion(
        self, 
        sesion: SesionAprendizaje, 
        session: AsyncSession
    ) -> SesionAprendizajeEntity:
        new_sesion = SesionAprendizajeEntity(
            unidad_id=sesion.unidad_id,
            tema=sesion.tema,
            fecha_dictado=sesion.fecha_dictado,
            numero_sesion=sesion.numero_sesion
        )
        session.add(new_sesion)
        await session.commit()
        await session.refresh(new_sesion)
        return new_sesion

    async def update_sesion(
        self, 
        sesion_id: int, 
        sesion: UpdateSesionAprendizaje, 
        session: AsyncSession
    ) -> SesionAprendizajeEntity:
        db_sesion = await self.get_sesion_by_id(sesion_id, session)
        
        update_data = sesion.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_sesion, key, value)

        await session.commit()
        await session.refresh(db_sesion)
        return db_sesion

    async def delete_sesion(
        self, 
        sesion_id: int, 
        session: AsyncSession
    ) -> bool:
        sesion = await self.get_sesion_by_id(sesion_id, session)
        await session.delete(sesion)
        await session.commit()
        return True