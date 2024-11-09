from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .input_service import InputService
from .input_model import Input, UpdateInput

@Controller("inputs")
class InputController:
    def __init__(self, input_service: InputService):
        self.input_service = input_service

    @Get("/")
    async def get_inputs(self, session: AsyncSession = Depends(config.get_db)):
        return await self.input_service.get_inputs(session)
        
    @Get("/{input_id}")
    async def get_input(self, input_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.input_service.get_input_by_id(input_id, session)
        
    @Post("/")
    async def create_input(self, input_data: Input, session: AsyncSession = Depends(config.get_db)):
        return await self.input_service.create_input(input_data, session)
        
    @Put("/{input_id}")
    async def update_input(self, input_id: int, input_data: UpdateInput, session: AsyncSession = Depends(config.get_db)):
        return await self.input_service.update_input(input_id, input_data, session)
        
    @Delete("/{input_id}")
    async def delete_input(self, input_id: int, session: AsyncSession = Depends(config.get_db)):
        return await self.input_service.delete_input(input_id, session)