from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from .curso_usuario_entity import CursoUsuarioEntity
from .curso_usuario_model import CursoUsuario, UpdateCursoUsuario
from datetime import date

@Injectable()
class CursoUsuarioService:
    async def get_asignaciones(self, session: AsyncSession) -> List[CursoUsuarioEntity]:
        query = select(CursoUsuarioEntity)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_curso(
        self,
        curso_id: int,
        session: AsyncSession
    ) -> List[CursoUsuarioEntity]:
        query = select(CursoUsuarioEntity).where(
            CursoUsuarioEntity.curso_id == curso_id
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_usuario(
        self,
        usuario_id: int,
        session: AsyncSession
    ) -> List[CursoUsuarioEntity]:
        query = select(CursoUsuarioEntity).where(
            CursoUsuarioEntity.usuario_id == usuario_id
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_id(
        self, 
        curso_usuario_id: int, 
        session: AsyncSession
    ) -> CursoUsuarioEntity:
        query = select(CursoUsuarioEntity).where(
            CursoUsuarioEntity.curso_usuario_id == curso_usuario_id
        )
        result = await session.execute(query)
        curso_usuario = result.scalar_one_or_none()
        
        if not curso_usuario:
            raise HTTPException(
                status_code=404, 
                detail="Asignación curso-usuario no encontrada"
            )
        return curso_usuario

    async def create_asignacion(
        self, 
        curso_usuario: CursoUsuario, 
        session: AsyncSession
    ) -> CursoUsuarioEntity:
        new_asignacion = CursoUsuarioEntity(
            curso_id=curso_usuario.curso_id,
            usuario_id=curso_usuario.usuario_id,
            fecha_asignacion=curso_usuario.fecha_asignacion or date.today()
        )
        session.add(new_asignacion)
        await session.commit()
        await session.refresh(new_asignacion)
        return new_asignacion

    async def update_asignacion(
        self, 
        curso_usuario_id: int, 
        curso_usuario: UpdateCursoUsuario, 
        session: AsyncSession
    ) -> CursoUsuarioEntity:
        db_asignacion = await self.get_by_id(curso_usuario_id, session)
        
        if curso_usuario.fecha_asignacion:
            db_asignacion.fecha_asignacion = curso_usuario.fecha_asignacion

        await session.commit()
        await session.refresh(db_asignacion)
        return db_asignacion

    async def delete_asignacion(
        self, 
        curso_usuario_id: int, 
        session: AsyncSession
    ) -> bool:
        asignacion = await self.get_by_id(curso_usuario_id, session)
        await session.delete(asignacion)
        await session.commit()
        return True