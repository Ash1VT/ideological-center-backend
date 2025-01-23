from typing import Optional

from fastapi import APIRouter, Query, Depends

from core.dependencies.uow.sqlalchemy import get_uow, get_uow_with_commit
from core.errors.handler import handle_app_errors
from core.pagination.schema import PaginatedOut
from core.uow.generic import GenericUnitOfWork
from db.sqlalchemy.models import User
from modules.media.dependencies.services import get_media_category_service
from modules.media.schemas import MediaCategoryRetrieveOutSchema, MediaCategoryCreateOutSchema, \
    MediaCategoryUpdateOutSchema, MediaCategoryCreateInSchema, MediaCategoryUpdateInSchema
from modules.media.services import MediaCategoryService
from modules.users.auth import fastapi_users

media_category_router = APIRouter(prefix="/media/categories", tags=["media_category"])


@media_category_router.get("/", response_model=PaginatedOut[MediaCategoryRetrieveOutSchema])
@handle_app_errors
async def retrieve_all(page: Optional[int] = Query(None),
                       per_page: Optional[int] = Query(None),
                       service: MediaCategoryService = Depends(get_media_category_service),
                       uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve_all(page=page, per_page=per_page, uow=uow)


@media_category_router.get("/{id}", response_model=MediaCategoryRetrieveOutSchema)
@handle_app_errors
async def retrieve(id: int,
                   service: MediaCategoryService = Depends(get_media_category_service),
                   uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve(id=id, uow=uow)


@media_category_router.post("/", response_model=MediaCategoryCreateOutSchema)
@handle_app_errors
async def create(media_category: MediaCategoryCreateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MediaCategoryService = Depends(get_media_category_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.create(item=media_category, uow=uow)


@media_category_router.put("/{id}", response_model=MediaCategoryUpdateOutSchema)
@handle_app_errors
async def update(id: int,
                 media_category: MediaCategoryUpdateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MediaCategoryService = Depends(get_media_category_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.update(id=id, item=media_category, uow=uow)


@media_category_router.delete("/{id}")
@handle_app_errors
async def delete(id: int,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MediaCategoryService = Depends(get_media_category_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    await service.delete(id=id, uow=uow)
    return {}


@media_category_router.post("/{category_id}/media/{media_id}")
@handle_app_errors
async def add_media_to_category(category_id: int,
                                media_id: int,
                                admin: User = Depends(fastapi_users.current_user(superuser=True)),
                                service: MediaCategoryService = Depends(get_media_category_service),
                                uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    await service.add_media_to_category(category_id=category_id, media_id=media_id, uow=uow)
    return {}


@media_category_router.delete("/{category_id}/media/{media_id}")
@handle_app_errors
async def remove_media_from_category(category_id: int,
                                     media_id: int,
                                     admin: User = Depends(fastapi_users.current_user(superuser=True)),
                                     service: MediaCategoryService = Depends(get_media_category_service),
                                     uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    await service.remove_media_from_category(category_id=category_id, media_id=media_id, uow=uow)
    return {}
