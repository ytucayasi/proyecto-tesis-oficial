from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from .tipo_secuencia_entity import TipoSecuenciaEntity
from .tipo_secuencia_model import TipoSecuencia, UpdateTipoSecuencia

@Injectable()
class TipoSecuenciaService:
    async def get_tipos_secuencia(self, session: AsyncSession) -> List[TipoSecuenciaEntity]:
        query = select(TipoSecuenciaEntity)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_tipo_secuencia_by_id(
        self, 
        tipo_id: int, 
        session: AsyncSession
    ) -> TipoSecuenciaEntity:
        query = select(TipoSecuenciaEntity).where(
            TipoSecuenciaEntity.tipo_secuencia_id == tipo_id
        )
        result = await session.execute(query)
        tipo_secuencia = result.scalar_one_or_none()
        
        if not tipo_secuencia:
            raise HTTPException(
                status_code=404, 
                detail="Tipo de secuencia no encontrado"
            )
        return tipo_secuencia

    async def create_tipo_secuencia(
        self, 
        tipo_secuencia: TipoSecuencia, 
        session: AsyncSession
    ) -> TipoSecuenciaEntity:
        new_tipo_secuencia = TipoSecuenciaEntity(
            nombre=tipo_secuencia.nombre,
            descripcion=tipo_secuencia.descripcion
        )
        session.add(new_tipo_secuencia)
        await session.commit()
        await session.refresh(new_tipo_secuencia)
        return new_tipo_secuencia

    async def update_tipo_secuencia(
        self, 
        tipo_id: int, 
        tipo_secuencia: UpdateTipoSecuencia, 
        session: AsyncSession
    ) -> TipoSecuenciaEntity:
        db_tipo_secuencia = await self.get_tipo_secuencia_by_id(tipo_id, session)
        
        update_data = tipo_secuencia.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_tipo_secuencia, key, value)

        await session.commit()
        await session.refresh(db_tipo_secuencia)
        return db_tipo_secuencia

    async def delete_tipo_secuencia(
        self, 
        tipo_id: int, 
        session: AsyncSession
    ) -> bool:
        tipo_secuencia = await self.get_tipo_secuencia_by_id(tipo_id, session)
        await session.delete(tipo_secuencia)
        await session.commit()
        return True