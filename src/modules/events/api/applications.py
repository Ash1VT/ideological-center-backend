from fastapi import APIRouter, Depends

from core.dependencies.uow.sqlalchemy import get_uow, get_uow_with_commit
from core.errors.handler import handle_app_errors
from core.uow.generic import GenericUnitOfWork
from db.sqlalchemy.models import User
from modules.events.dependencies.services import get_event_application_service
from modules.events.schemas import EventApplicationRetrieveOutSchema, EventApplicationUpdateOutSchema, \
    EventApplicationUpdateInSchema
from modules.events.services import EventApplicationService
from modules.users.auth import fastapi_users

events_applications_router = APIRouter(prefix="/events/applications", tags=["events_applications"])


@events_applications_router.get("/{id}", response_model=EventApplicationRetrieveOutSchema)
@handle_app_errors
async def retrieve(id: int,
                   service: EventApplicationService = Depends(get_event_application_service),
                   uow: GenericUnitOfWork = Depends(get_uow)):
    return await service.retrieve(id=id, uow=uow)


@events_applications_router.put("/{id}", response_model=EventApplicationUpdateOutSchema)
@handle_app_errors
async def update(id: int,
                 item: EventApplicationUpdateInSchema,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: EventApplicationService = Depends(get_event_application_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    return await service.update(id=id, item=item, uow=uow)


@events_applications_router.delete("/{id}")
@handle_app_errors
async def delete(id: int,
                 admin: User = Depends(fastapi_users.current_user(superuser=True)),
                 service: EventApplicationService = Depends(get_event_application_service),
                 uow: GenericUnitOfWork = Depends(get_uow_with_commit)):
    await service.delete(id=id, uow=uow)
    return {}
