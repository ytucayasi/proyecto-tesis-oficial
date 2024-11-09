from nest.core import Controller, Get, Post, Put, Delete, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from .curso_usuario_service import CursoUsuarioService
from .curso_usuario_model import (
    CursoUsuario,
    UpdateCursoUsuario,
    CursoUsuarioResponse
)
from typing import List

@Controller("curso-usuarios")
class CursoUsuarioController:
    def __init__(self, curso_usuario_service: CursoUsuarioService):
        self.curso_usuario_service = curso_usuario_service

    @Get("/")
    async def get_asignaciones(
        self, 
        session: AsyncSession = Depends(config.get_db)
    ) -> List[CursoUsuarioResponse]:
        return await self.curso_usuario_service.get_asignaciones(session)
    
    @Get("/curso/:curso_id/")
    async def get_by_curso(
        self,
        curso_id: int,
        session: AsyncSession = Depends(config.get_db)
    ) -> List[CursoUsuarioResponse]:
        return await self.curso_usuario_service.get_by_curso(curso_id, session)

    @Get("/usuario/:usuario_id/")
    async def get_by_usuario(
        self,
        usuario_id: int,
        session: AsyncSession = Depends(config.get_db)
    ) -> List[CursoUsuarioResponse]:
        return await self.curso_usuario_service.get_by_usuario(usuario_id, session)
        
    @Get("/:curso_usuario_id/")
    async def get_asignacion(
        self, 
        curso_usuario_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ) -> CursoUsuarioResponse:
        return await self.curso_usuario_service.get_by_id(
            curso_usuario_id, 
            session
        )
        
    @Post("/")
    async def create_asignacion(
        self, 
        curso_usuario: CursoUsuario, 
        session: AsyncSession = Depends(config.get_db)
    ) -> CursoUsuarioResponse:
        return await self.curso_usuario_service.create_asignacion(
            curso_usuario, 
            session
        )
        
    @Put("/:curso_usuario_id/")
    async def update_asignacion(
        self, 
        curso_usuario_id: int, 
        curso_usuario: UpdateCursoUsuario, 
        session: AsyncSession = Depends(config.get_db)
    ) -> CursoUsuarioResponse:
        return await self.curso_usuario_service.update_asignacion(
            curso_usuario_id, 
            curso_usuario, 
            session
        )
        
    @Delete("/:curso_usuario_id/")
    async def delete_asignacion(
        self, 
        curso_usuario_id: int, 
        session: AsyncSession = Depends(config.get_db)
    ):
        await self.curso_usuario_service.delete_asignacion(curso_usuario_id, session)
        return {"message": "Asignación curso-usuario eliminada exitosamente"}