from .ejemplos_model import Ejemplos
from .ejemplos_entity import Ejemplos as EjemplosEntity
from nest.core.decorators.database import async_db_request_handler
from nest.core import Injectable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

@Injectable
class EjemplosService:

    @async_db_request_handler
    async def add_ejemplos(self, ejemplos: Ejemplos, session: AsyncSession):
        new_ejemplos = EjemplosEntity(
            **ejemplos.dict()
        )
        session.add(new_ejemplos)
        await session.commit()
        return new_ejemplos.id

    @async_db_request_handler
    async def get_ejemplos(self, session: AsyncSession):
        query = select(EjemplosEntity)
        result = await session.execute(query)
        return result.scalars().all()