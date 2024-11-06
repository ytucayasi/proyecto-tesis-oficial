from nest.core import Injectable
from nest.core.decorators.database import async_db_request_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException
from .personas_model import Persona, UpdatePersona
from .personas_entity import Persona as PersonaEntity

@Injectable
class PersonasService:
    @async_db_request_handler
    async def create_persona(self, persona: Persona, session: AsyncSession):
        new_persona = PersonaEntity(**persona.dict())
        session.add(new_persona)
        await session.commit()
        await session.refresh(new_persona)
        return new_persona

    @async_db_request_handler
    async def get_personas(self, session: AsyncSession):
        query = select(PersonaEntity)
        result = await session.execute(query)
        return result.scalars().all()

    @async_db_request_handler
    async def get_persona_by_id(self, persona_id: int, session: AsyncSession):
        query = select(PersonaEntity).where(PersonaEntity.persona_id == persona_id)
        result = await session.execute(query)
        persona = result.scalar_one_or_none()
        
        if persona is None:
            raise HTTPException(status_code=404, detail=f"Persona with id {persona_id} not found")
            
        return persona

    @async_db_request_handler
    async def update_persona(self, persona_id: int, persona_update: UpdatePersona, session: AsyncSession):
        # Verificar si existe
        await self.get_persona_by_id(persona_id, session)
        
        # Filtrar campos no nulos
        update_data = persona_update.dict(exclude_unset=True)
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Actualizar
        query = update(PersonaEntity).where(PersonaEntity.persona_id == persona_id).values(**update_data)
        await session.execute(query)
        await session.commit()
        
        return await self.get_persona_by_id(persona_id, session)

    @async_db_request_handler
    async def delete_persona(self, persona_id: int, session: AsyncSession):
        await self.get_persona_by_id(persona_id, session)
        query = delete(PersonaEntity).where(PersonaEntity.persona_id == persona_id)
        await session.execute(query)
        await session.commit()
        return {"message": f"Persona with id {persona_id} has been deleted"}