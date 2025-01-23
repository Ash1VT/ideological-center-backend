from typing import Optional

from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException

from core.dependencies.uow.sqlalchemy import get_uow, get_uow_with_commit
from core.errors.handler import handle_app_errors
from core.pagination.schema import PaginatedOut
from core.uow.generic import GenericUnitOfWork
from db.sqlalchemy.models import User
from modules.museum.dependencies.services import get_museum_hall_service, get_museum_section_service
from modules.museum.schemas import MuseumHallRetrieveOutSchema, MuseumHallCreateOutSchema, MuseumHallUpdateOutSchema, \
    MuseumHallCreateInSchema, MuseumHallUpdateInSchema, MuseumSectionCreateOutSchema, MuseumSectionCreateInSchema, \
    MuseumSectionRetrieveOutSchema
from modules.museum.services import MuseumHallService, MuseumSectionService
from modules.users.auth import fastapi_users

museum_hall_router = APIRouter(prefix="/museum/halls", tags=["museum_halls"])


@museum_hall_router.get("/", response_model=PaginatedOut[MuseumHallRetrieveOutSchema])
@handle_app_errors
async def retrieve_all(page: Optional[int] = Query(None),
                       per_page: Optional[int] = Query(None),
                       service: MuseumHallService = Depends(get_museum_hall_service),
                       uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve_all(page=page,
                                      per_page=per_page,
                                      uow=uow)


@museum_hall_router.get("/{id}", response_model=MuseumHallRetrieveOutSchema)
@handle_app_errors
async def retrieve(id: int,
                   service: MuseumHallService = Depends(get_museum_hall_service),
                   uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve(id=id, uow=uow)


@museum_hall_router.post("/", response_model=MuseumHallCreateOutSchema)
@handle_app_errors
async def create(hall: MuseumHallCreateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MuseumHallService = Depends(get_museum_hall_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.create(item=hall, uow=uow)


@museum_hall_router.put("/{id}", response_model=MuseumHallUpdateOutSchema)
@handle_app_errors
async def update(id: int,
                 hall: MuseumHallUpdateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MuseumHallService = Depends(get_museum_hall_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.update(id=id, item=hall, uow=uow)


@museum_hall_router.delete("/{id}")
@handle_app_errors
async def delete(id: int,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MuseumHallService = Depends(get_museum_hall_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    await service.delete(id=id, uow=uow)
    return {}


@museum_hall_router.get("/{hall_id}/sections", response_model=PaginatedOut[MuseumSectionRetrieveOutSchema])
@handle_app_errors
async def retrieve_all_sections(hall_id: int,
                                page: Optional[int] = Query(None),
                                per_page: Optional[int] = Query(None),
                                service: MuseumSectionService = Depends(get_museum_section_service),
                                uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.retrieve_all(hall_id=hall_id, page=page, per_page=per_page, uow=uow)


@museum_hall_router.post("/{hall_id}/sections", response_model=MuseumSectionCreateOutSchema)
@handle_app_errors
async def create_section(hall_id: int,
                         section: MuseumSectionCreateInSchema,
                         admin: User = Depends(fastapi_users.current_user(superuser=True)),
                         service: MuseumSectionService = Depends(get_museum_section_service),
                         uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.create(hall_id=hall_id, item=section, uow=uow)


@museum_hall_router.put("/{id}/image/upload", response_model=MuseumHallUpdateOutSchema)
@handle_app_errors
async def upload_image(id: int,
                       admin: User = Depends(fastapi_users.current_user(superuser=True)),
                       image: UploadFile = File(...),
                       service: MuseumHallService = Depends(get_museum_hall_service),
                       uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    if not image.content_type.startswith('image'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    return await service.upload_image(id=id, image=image, uow=uow)
