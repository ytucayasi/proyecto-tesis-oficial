from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from .cursos_model import Curso, UpdateCurso
from .cursos_entity import Curso as CursoEntity

@Injectable
class CursosService:
    @async_db_request_handler
    async def create_curso(self, curso: Curso, session: AsyncSession):
        new_curso = CursoEntity(**curso.dict())
        session.add(new_curso)
        await session.commit()
        await session.refresh(new_curso)
        return new_curso

    @async_db_request_handler
    async def get_cursos(self, session: AsyncSession):
        query = select(CursoEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_curso_by_id(self, curso_id: int, session: AsyncSession):
        query = select(CursoEntity).where(CursoEntity.curso_id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()

        if curso is None:
            raise HTTPException(status_code=404, detail=f"Curso with id {curso_id} not found")

        return curso

    @async_db_request_handler
    async def update_curso(self, curso_id: int, curso_update: UpdateCurso, session: AsyncSession):
        await self.get_curso_by_id(curso_id, session)
        update_data = curso_update.dict(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")

        query = update(CursoEntity).where(CursoEntity.curso_id == curso_id).values(**update_data)
        await session.execute(query)
        await session.commit()

        return await self.get_curso_by_id(curso_id, session)

    @async_db_request_handler
    async def delete_curso(self, curso_id: int, session: AsyncSession):
        await self.get_curso_by_id(curso_id, session)
        query = delete(CursoEntity).where(CursoEntity.curso_id == curso_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Curso with id {curso_id} has been deleted"}
