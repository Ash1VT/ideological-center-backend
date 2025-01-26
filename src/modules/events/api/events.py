import datetime
from typing import Optional, List

from fastapi import APIRouter, Query, Depends, UploadFile, File, HTTPException

from core.dependencies.uow.sqlalchemy import get_uow, get_uow_with_commit
from core.errors.handler import handle_app_errors
from core.pagination.schema import PaginatedOut
from core.uow.generic import GenericUnitOfWork
from db.sqlalchemy.models import EventApplicationStatus, User
from modules.events.dependencies.services import get_event_service, get_event_application_service
from modules.events.schemas import EventRetrieveOutSchema, EventCreateOutSchema, EventCreateInSchema, \
    EventUpdateInSchema, EventUpdateOutSchema, EventApplicationRetrieveOutSchema, EventApplicationCreateOutSchema, \
    EventApplicationCreateInSchema
from modules.events.services import EventService, EventApplicationService
from modules.users.auth import fastapi_users

events_router = APIRouter(prefix="/events", tags=["events"])


@events_router.get("/", response_model=PaginatedOut[EventRetrieveOutSchema])
@handle_app_errors
async def retrieve_all(page: int = Query(None),
                       per_page: int = Query(None),
                       name_contains: Optional[str] = Query(None),
                       start_dt: Optional[datetime.date] = Query(None),
                       end_dt: Optional[datetime.date] = Query(None),
                       service: EventService = Depends(get_event_service),
                       uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve_all(page=page,
                                      per_page=per_page,
                                      name_contains=name_contains,
                                      start_dt=start_dt,
                                      end_dt=end_dt,
                                      uow=uow)


@events_router.get("/{id}", response_model=EventRetrieveOutSchema)
@handle_app_errors
async def retrieve(id: int,
                   service: EventService = Depends(get_event_service),
                   uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve(id=id, uow=uow)


@events_router.post("/", response_model=EventCreateOutSchema)
@handle_app_errors
async def create(event: EventCreateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: EventService = Depends(get_event_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.create(item=event, uow=uow)


@events_router.put("/{id}", response_model=EventUpdateOutSchema)
@handle_app_errors
async def update(id: int,
                 event: EventUpdateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: EventService = Depends(get_event_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.update(id=id, item=event, uow=uow)


@events_router.delete("/{id}")
@handle_app_errors
async def delete(id: int,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: EventService = Depends(get_event_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    await service.delete(id=id, uow=uow)
    return {}


@events_router.put("/{id}/image/upload", response_model=EventUpdateOutSchema)
@handle_app_errors
async def upload_image(id: int,
                       image: UploadFile = File(...),
                       admin: User = Depends(fastapi_users.current_user(superuser=True)),
                       service: EventService = Depends(get_event_service),
                       uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    if not image.content_type.startswith('image'):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    return await service.upload_image(id=id, image=image, uow=uow)


@events_router.get("/{event_id}/applications", response_model=PaginatedOut[EventApplicationRetrieveOutSchema])
@handle_app_errors
async def retrieve_event_applications(event_id: int,
                                      page: int = Query(None),
                                      per_page: int = Query(None),
                                      fio_contains: Optional[str] = Query(None),
                                      statuses: Optional[List[EventApplicationStatus]] = Query(None),
                                      service: EventApplicationService = Depends(get_event_application_service),
                                      uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve_all(page=page,
                                      per_page=per_page,
                                      fio_contains=fio_contains,
                                      statuses=statuses,
                                      event_id=event_id,
                                      uow=uow)


@events_router.post("/{event_id}/applications", response_model=EventApplicationCreateOutSchema)
@handle_app_errors
async def create_event_application(event_id: int,
                                   application: EventApplicationCreateInSchema,
                                   service: EventApplicationService = Depends(get_event_application_service),
                                   uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.create(event_id=event_id, item=application, uow=uow)
