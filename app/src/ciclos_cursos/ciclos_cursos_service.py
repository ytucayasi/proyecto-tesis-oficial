from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from .ciclos_cursos_model import CicloCurso, UpdateCicloCurso
from .ciclos_cursos_entity import CicloCurso as CicloCursoEntity

@Injectable
class CiclosCursosService:
    @async_db_request_handler
    async def create_ciclo_curso(self, ciclo_curso: CicloCurso, session: AsyncSession):
        new_ciclo_curso = CicloCursoEntity(**ciclo_curso.dict())
        session.add(new_ciclo_curso)
        await session.commit()
        await session.refresh(new_ciclo_curso)
        return new_ciclo_curso

    @async_db_request_handler
    async def get_ciclos_cursos(self, session: AsyncSession):
        query = select(CicloCursoEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_ciclo_curso_by_id(self, ciclo_curso_id: int, session: AsyncSession):
        query = select(CicloCursoEntity).where(CicloCursoEntity.ciclo_curso_id == ciclo_curso_id)
        result = await session.execute(query)
        ciclo_curso = result.scalar_one_or_none()
        
        if ciclo_curso is None:
            raise HTTPException(status_code=404, detail=f"CicloCurso with id {ciclo_curso_id} not found")
            
        return ciclo_curso

    @async_db_request_handler
    async def update_ciclo_curso(self, ciclo_curso_id: int, ciclo_curso_update: UpdateCicloCurso, session: AsyncSession):
        await self.get_ciclo_curso_by_id(ciclo_curso_id, session)
        update_data = ciclo_curso_update.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        query = update(CicloCursoEntity).where(CicloCursoEntity.ciclo_curso_id == ciclo_curso_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        
        return await self.get_ciclo_curso_by_id(ciclo_curso_id, session)

    @async_db_request_handler
    async def delete_ciclo_curso(self, ciclo_curso_id: int, session: AsyncSession):
        await self.get_ciclo_curso_by_id(ciclo_curso_id, session)
        query = delete(CicloCursoEntity).where(CicloCursoEntity.ciclo_curso_id == ciclo_curso_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"CicloCurso with id {ciclo_curso_id} has been deleted"}
