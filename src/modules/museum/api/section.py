from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from core.dependencies.uow.sqlalchemy import get_uow, get_uow_with_commit
from core.errors.handler import handle_app_errors
from core.uow.generic import GenericUnitOfWork
from db.sqlalchemy.models import User
from modules.museum.dependencies.services import get_museum_section_service
from modules.museum.schemas import MuseumSectionRetrieveOutSchema, MuseumSectionCreateInSchema, \
    MuseumSectionUpdateOutSchema, MuseumSectionUpdateInSchema
from modules.museum.services import MuseumSectionService
from modules.users.auth import fastapi_users

museum_section_router = APIRouter(prefix="/museum/sections", tags=["museum_sections"])


@museum_section_router.get("/{id}", response_model=MuseumSectionRetrieveOutSchema)
@handle_app_errors
async def retrieve(id: int,
                   service: MuseumSectionService = Depends(get_museum_section_service),
                   uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve(id=id, uow=uow)


@museum_section_router.put("/{id}", response_model=MuseumSectionUpdateOutSchema)
@handle_app_errors
async def update(id: int,
                 hall: MuseumSectionUpdateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MuseumSectionService = Depends(get_museum_section_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.update(id=id, item=hall, uow=uow)


@museum_section_router.delete("/{id}")
@handle_app_errors
async def delete(id: int,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MuseumSectionService = Depends(get_museum_section_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    await service.delete(id=id, uow=uow)
    return {}


@museum_section_router.put("/{id}/image/upload", response_model=MuseumSectionUpdateOutSchema)
@handle_app_errors
async def upload_image(id: int,
                       image: UploadFile = File(...),
                       admin: User = Depends(fastapi_users.current_user(superuser=True)),
                       service: MuseumSectionService = Depends(get_museum_section_service),
                       uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    if not image.content_type.startswith('image'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    return await service.upload_image(id=id, image=image, uow=uow)
