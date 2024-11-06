from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .personas_service import PersonasService
from .personas_model import Persona, UpdatePersona

@Controller("personas")
class PersonasController:
    def __init__(self, personas_service: PersonasService):
        self.personas_service = personas_service

    @Get("/")
    async def get_personas(self, session: AsyncSession = Depends(config.get_db)):
        return await self.personas_service.get_personas(session)
        
    @Get("/{persona_id}")
    async def get_persona(self, persona_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.personas_service.get_persona_by_id(persona_id, session)
        
    @Post("/")
    async def create_persona(self, persona: Persona, session: AsyncSession = Depends(config.get_db)):
        return await self.personas_service.create_persona(persona, session)
        
    @Put("/{persona_id}")
    async def update_persona(self, persona_id: int, persona: UpdatePersona, session: AsyncSession = Depends(config.get_db)):
        return await self.personas_service.update_persona(persona_id, persona, session)
        
    @Delete("/{persona_id}")
    async def delete_persona(self, persona_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.personas_service.delete_persona(persona_id, session)