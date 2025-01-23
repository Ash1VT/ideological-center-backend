from typing import Optional, List

from fastapi import APIRouter, Query, Depends, UploadFile, File, HTTPException, Form

from core.dependencies.uow.sqlalchemy import get_uow, get_uow_with_commit
from core.errors.handler import handle_app_errors
from core.pagination.schema import PaginatedOut
from core.uow.generic import GenericUnitOfWork
from db.sqlalchemy.models import MediaType, User
from modules.media.dependencies.services import get_media_service, get_media_photo_service
from modules.media.schemas import MediaRetrieveOutSchema, MediaCreateInSchema, MediaCreateOutSchema, \
    MediaUpdateInSchema, MediaUpdateOutSchema, MediaPhotoRetrieveOutSchema
from modules.media.services import MediaService, MediaPhotoService
from modules.users.auth import fastapi_users

media_router = APIRouter(prefix="/media", tags=["media"])


@media_router.get("/", response_model=PaginatedOut[MediaRetrieveOutSchema])
@handle_app_errors
async def retrieve_all(page: Optional[int] = Query(None),
                       per_page: Optional[int] = Query(None),
                       name_contains: Optional[str] = Query(None),
                       types: Optional[List[MediaType]] = Query(None),
                       category_id: Optional[int] = Query(None),
                       service: MediaService = Depends(get_media_service),
                       uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve_all(page=page,
                                      per_page=per_page,
                                      name_contains=name_contains,
                                      types=types,
                                      category_id=category_id,
                                      uow=uow)


@media_router.get("/{id}", response_model=MediaRetrieveOutSchema)
@handle_app_errors
async def retrieve(id: int,
                   service: MediaService = Depends(get_media_service),
                   uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve(id=id, uow=uow)


@media_router.post("/", response_model=MediaCreateOutSchema)
@handle_app_errors
async def create(media: MediaCreateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MediaService = Depends(get_media_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.create(item=media, uow=uow)


@media_router.put("/{id}", response_model=MediaUpdateOutSchema)
@handle_app_errors
async def update(id: int,
                 media: MediaUpdateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MediaService = Depends(get_media_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.update(id=id, item=media, uow=uow)


@media_router.delete("/{id}")
@handle_app_errors
async def delete(id: int,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: MediaService = Depends(get_media_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    await service.delete(id=id, uow=uow)
    return {}


@media_router.put("/{id}/image/upload", response_model=MediaUpdateOutSchema)
@handle_app_errors
async def upload_image(id: int,
                       image: UploadFile = File(...),
                       admin: User = Depends(fastapi_users.current_user(superuser=True)),
                       service: MediaService = Depends(get_media_service),
                       uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    if not image.content_type.startswith('image'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    return await service.upload_image(id=id, image=image, uow=uow)


@media_router.put("/{id}/file/upload", response_model=MediaUpdateOutSchema)
@handle_app_errors
async def upload_file(id: int,
                      file: UploadFile = File(...),
                      admin: User = Depends(fastapi_users.current_user(superuser=True)),
                      service: MediaService = Depends(get_media_service),
                      uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.upload_file(id=id, file=file, uow=uow)


@media_router.post("/{media_id}/photos", response_model=MediaPhotoRetrieveOutSchema)
@handle_app_errors
async def create_photo(media_id: int,
                       image: UploadFile = File(...),
                       admin: User = Depends(fastapi_users.current_user(superuser=True)),
                       service: MediaPhotoService = Depends(get_media_photo_service),
                       uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    if not image.content_type.startswith('image'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    return await service.create(media_id=media_id, image=image, uow=uow)


@media_router.delete("/photos/{photo_id}")
@handle_app_errors
async def delete_photo(photo_id: int,
                       admin: User = Depends(fastapi_users.current_user(superuser=True)),
                       service: MediaPhotoService = Depends(get_media_photo_service),
                       uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    await service.delete(id=photo_id, uow=uow)
    return {}
