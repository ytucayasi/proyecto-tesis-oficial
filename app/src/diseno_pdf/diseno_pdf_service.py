from nest.core import Injectable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from .diseno_pdf_entity import DisenoPdfEntity
from .diseno_pdf_model import DisenoPdf, UpdateDisenoPdf

@Injectable()
class DisenoPdfService:
    async def get_diseno_pdfs(self, session: AsyncSession) -> List[DisenoPdfEntity]:
        query = select(DisenoPdfEntity)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_diseno_pdf_by_id(
        self, 
        diseno_pdf_id: int, 
        session: AsyncSession
    ) -> DisenoPdfEntity:
        query = select(DisenoPdfEntity).where(
            DisenoPdfEntity.diseno_pdf_id == diseno_pdf_id
        )
        result = await session.execute(query)
        diseno_pdf = result.scalar_one_or_none()
        
        if not diseno_pdf:
            raise HTTPException(
                status_code=404, 
                detail="Diseño PDF no encontrado"
            )
        return diseno_pdf

    async def create_diseno_pdf(
        self, 
        diseno_pdf: DisenoPdf, 
        session: AsyncSession
    ) -> DisenoPdfEntity:
        new_diseno_pdf = DisenoPdfEntity(
            nombre=diseno_pdf.nombre,
            link_archivo=diseno_pdf.link_archivo,
            estado=diseno_pdf.estado
        )
        session.add(new_diseno_pdf)
        await session.commit()
        await session.refresh(new_diseno_pdf)
        return new_diseno_pdf

    async def update_diseno_pdf(
        self, 
        diseno_pdf_id: int, 
        diseno_pdf: UpdateDisenoPdf, 
        session: AsyncSession
    ) -> DisenoPdfEntity:
        db_diseno_pdf = await self.get_diseno_pdf_by_id(diseno_pdf_id, session)
        
        update_data = diseno_pdf.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_diseno_pdf, key, value)

        await session.commit()
        await session.refresh(db_diseno_pdf)
        return db_diseno_pdf

    async def delete_diseno_pdf(
        self, 
        diseno_pdf_id: int, 
        session: AsyncSession
    ) -> bool:
        diseno_pdf = await self.get_diseno_pdf_by_id(diseno_pdf_id, session)
        await session.delete(diseno_pdf)
        await session.commit()
        return True