from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from .generacion_recurso_entity import GeneracionRecursoEntity
from .generacion_recurso_model import GeneracionRecurso, UpdateGeneracionRecurso

@Injectable()
class GeneracionRecursoService:
    async def get_generaciones(self, session: AsyncSession) -> List[GeneracionRecursoEntity]:
        query = select(GeneracionRecursoEntity)
        result = await session.execute(query)
        return result.scalars().all()

    # async def get_by_secuencia(
    #     self,
    #     secuencia_id: int,
    #     session: AsyncSession
    # ) -> List[GeneracionRecursoEntity]:
    #     query = select(GeneracionRecursoEntity).where(
    #         GeneracionRecursoEntity.secuencia_aprendizaje_id == secuencia_id
    #     )
    #     result = await session.execute(query)
    #     return result.scalars().all()

    # async def get_by_usuario(
    #     self,
    #     usuario_id: int,
    #     session: AsyncSession
    # ) -> List[GeneracionRecursoEntity]:
    #     query = select(GeneracionRecursoEntity).where(
    #         GeneracionRecursoEntity.usuario_id == usuario_id
    #     )
    #     result = await session.execute(query)
    #     return result.scalars().all()

    async def get_by_id(
        self, 
        generacion_id: int, 
        session: AsyncSession
    ) -> GeneracionRecursoEntity:
        query = select(GeneracionRecursoEntity).where(
            GeneracionRecursoEntity.generacion_recurso_id == generacion_id
        )
        result = await session.execute(query)
        generacion = result.scalar_one_or_none()
        
        if not generacion:
            raise HTTPException(
                status_code=404, 
                detail="Generación de recurso no encontrada"
            )
        return generacion

    async def create_generacion(
        self, 
        generacion: GeneracionRecurso, 
        session: AsyncSession
    ) -> GeneracionRecursoEntity:
        new_generacion = GeneracionRecursoEntity(
            input_id=generacion.input_id,
            diseno_id=generacion.diseno_id,
            numero_paginas=generacion.numero_paginas,
            tipo_documento=generacion.tipo_documento,
            link_archivo=generacion.link_archivo
        )
        session.add(new_generacion)
        await session.commit()
        await session.refresh(new_generacion)
        return new_generacion

    async def update_generacion(
        self, 
        generacion_id: int, 
        generacion: UpdateGeneracionRecurso, 
        session: AsyncSession
    ) -> GeneracionRecursoEntity:
        db_generacion = await self.get_by_id(generacion_id, session)
        
        update_data = generacion.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_generacion, key, value)

        await session.commit()
        await session.refresh(db_generacion)
        return db_generacion

    async def delete_generacion(
        self, 
        generacion_id: int, 
        session: AsyncSession
    ) -> bool:
        generacion = await self.get_by_id(generacion_id, session)
        await session.delete(generacion)
        await session.commit()
        return True