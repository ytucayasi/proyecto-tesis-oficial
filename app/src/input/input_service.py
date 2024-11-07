from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from .input_entity import InputEntity
from .input_model import Input, UpdateInput
from datetime import datetime
from typing import List
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

@Injectable()
class InputService:
    async def get_inputs(self, session: AsyncSession) -> List[InputEntity]:
        query = select(InputEntity)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_input_by_id(self, input_id: int, session: AsyncSession) -> InputEntity:
        query = select(InputEntity).where(InputEntity.input_id == input_id)
        result = await session.execute(query)
        input_item = result.scalar_one_or_none()
        
        if not input_item:
            raise HTTPException(status_code=404, detail="Input no encontrado")
        return input_item

    async def create_input(self, input_data: Input, session: AsyncSession) -> InputEntity:
        new_input = InputEntity(
            nombre=input_data.nombre,
            link_archivo=input_data.link_archivo
        )
        session.add(new_input)
        await session.commit()
        await session.refresh(new_input)
        return new_input

    async def update_input(self, input_id: int, input_data: UpdateInput, session: AsyncSession) -> InputEntity:
        input_item = await self.get_input_by_id(input_id, session)
        
        update_data = input_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(input_item, key, value)
        
        input_item.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(input_item)
        return input_item

    async def delete_input(self, input_id: int, session: AsyncSession) -> bool:
        input_item = await self.get_input_by_id(input_id, session)
        await session.delete(input_item)
        await session.commit()
        return True