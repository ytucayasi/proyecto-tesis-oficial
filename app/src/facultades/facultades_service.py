from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from .facultades_model import Facultad, UpdateFacultad
from .facultades_entity import Facultad as FacultadEntity

@Injectable
class FacultadesService:
    @async_db_request_handler
    async def create_facultad(self, facultad: Facultad, session: AsyncSession):
        new_facultad = FacultadEntity(**facultad.dict())
        session.add(new_facultad)
        await session.commit()
        await session.refresh(new_facultad)
        return new_facultad

    @async_db_request_handler
    async def get_facultades(self, session: AsyncSession):
        query = select(FacultadEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_facultad_by_id(self, facultad_id: int, session: AsyncSession):
        query = select(FacultadEntity).where(FacultadEntity.facultad_id == facultad_id)
        result = await session.execute(query)
        facultad = result.scalar_one_or_none()
        
        if facultad is None:
            raise HTTPException(status_code=404, detail=f"Facultad with id {facultad_id} not found")
            
        return facultad

    @async_db_request_handler
    async def update_facultad(self, facultad_id: int, facultad_update: UpdateFacultad, session: AsyncSession):
        # Verificar si existe
        await self.get_facultad_by_id(facultad_id, session)
        
        # Filtrar campos no nulos
        update_data = facultad_update.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Actualizar
        query = update(FacultadEntity).where(FacultadEntity.facultad_id == facultad_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        
        return await self.get_facultad_by_id(facultad_id, session)

    @async_db_request_handler
    async def delete_facultad(self, facultad_id: int, session: AsyncSession):
        await self.get_facultad_by_id(facultad_id, session)
        query = delete(FacultadEntity).where(FacultadEntity.facultad_id == facultad_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Facultad with id {facultad_id} has been deleted"}