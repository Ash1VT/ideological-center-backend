from dataclasses import asdict
from datetime import datetime
from typing import Optional, List

from fastapi import UploadFile, BackgroundTasks
from loguru import logger

from core.pagination.model import PaginatedModel
from core.pagination.schema import PaginatedOut
from core.services.mixins import RetrieveMixin, RetrieveAllMixin, CreateMixin, UpdateMixin, DeleteMixin
from core.uow.generic import GenericUnitOfWork
from db.sqlalchemy.models import Event, EventApplication, EventApplicationStatus
from modules.events.errors import EventNotFoundError, EventApplicationNotFoundError, EventAlreadyStartedError, \
    EventAlreadyFinishedError
from modules.events.schemas import EventRetrieveOutSchema, EventCreateOutSchema, EventCreateInSchema, \
    EventUpdateOutSchema, EventUpdateInSchema, EventApplicationCreateOutSchema, EventApplicationUpdateOutSchema, \
    EventApplicationUpdateInSchema, EventApplicationCreateInSchema, EventApplicationRetrieveOutSchema
from modules.events.utils.email import send_application_created_email, send_application_accepted_email, \
    send_application_rejected_email
from modules.events.utils.firebase import upload_event_image_to_firebase


class EventService(RetrieveMixin[Event, EventRetrieveOutSchema],
                   RetrieveAllMixin[Event, EventRetrieveOutSchema],
                   CreateMixin[Event, EventCreateInSchema, EventCreateOutSchema],
                   UpdateMixin[Event, EventUpdateInSchema, EventUpdateOutSchema],
                   DeleteMixin[Event]):
    schema_retrieve_out = EventRetrieveOutSchema
    schema_create_out = EventCreateOutSchema
    schema_update_out = EventUpdateOutSchema
    schema_paginated_out = PaginatedOut[EventRetrieveOutSchema]

    async def retrieve_instance(self, id: int, uow: GenericUnitOfWork, **kwargs) -> Event:
        instance = await uow.events.retrieve(id=id)

        if not instance:
            raise EventNotFoundError(id=id)

        return instance

    async def retrieve_all_instances(self,
                                     page: int,
                                     per_page: int,
                                     uow: GenericUnitOfWork,
                                     **kwargs) -> PaginatedModel[Event]:
        return await uow.events.retrieve_all(page=page, per_page=per_page)

    async def create_instance(self, item: EventCreateInSchema, uow: GenericUnitOfWork, **kwargs) -> Event:
        data = item.model_dump()
        return await uow.events.create(data=data)

    async def update_instance(self, id: int, item: EventUpdateInSchema, uow: GenericUnitOfWork, **kwargs) -> Event:
        data = item.model_dump()
        return await uow.events.update(id=id, data=data)

    async def delete_instance(self, id: int, uow: GenericUnitOfWork, **kwargs):
        instance = await uow.events.retrieve(id=id)

        if not instance:
            raise EventNotFoundError(id=id)

        await uow.events.delete(id=id)

    async def upload_image(self, id: int, image: UploadFile, uow: GenericUnitOfWork, **kwargs) -> EventUpdateOutSchema:
        instance = await uow.events.retrieve(id=id)

        if not instance:
            raise EventNotFoundError(id=id)

        image_url = upload_event_image_to_firebase(instance, image.filename, image.file)

        updated_instance = await uow.events.update(id, {
            'image_url': image_url
        })

        logger.info(f"Uploaded image for event with id={id}.")

        return self.schema_update_out.model_validate(updated_instance)


class EventApplicationService(RetrieveMixin[EventApplication, EventApplicationRetrieveOutSchema],
                              UpdateMixin[EventApplication,
                              EventApplicationUpdateInSchema,
                              EventApplicationUpdateOutSchema],
                              DeleteMixin[EventApplication]):
    schema_retrieve_out = EventApplicationRetrieveOutSchema
    schema_create_out = EventApplicationCreateOutSchema
    schema_update_out = EventApplicationUpdateOutSchema
    schema_paginated_out = PaginatedOut[EventApplicationRetrieveOutSchema]

    def __init__(self, background_tasks: BackgroundTasks):
        self._job_scheduler = background_tasks

    async def retrieve_instance(self, id: int, uow: GenericUnitOfWork, **kwargs) -> EventApplication:
        instance = await uow.events_applications.retrieve(id=id)

        if not instance:
            raise EventApplicationNotFoundError(id=id)

        return instance

    async def retrieve_all_instances(self,
                                     page: int,
                                     per_page: int,
                                     uow: GenericUnitOfWork,
                                     fio_contains: Optional[str] = None,
                                     statuses: Optional[List[int]] = None,
                                     event_id: Optional[int] = None,
                                     **kwargs) -> PaginatedModel[EventApplication]:
        return await uow.events_applications.retrieve_all(page=page, per_page=per_page, fio_contains=fio_contains,
                                                          statuses=statuses, event_id=event_id)

    async def create_instance(self, event_id: int, item: EventApplicationCreateInSchema, uow: GenericUnitOfWork,
                              **kwargs) -> EventApplication:
        event_instance = await uow.events.retrieve(id=event_id)

        if not event_instance:
            raise EventNotFoundError(id=event_id)

        # Check if event in time
        if event_instance.start_date < datetime.now().date() < event_instance.end_date:
            raise EventAlreadyStartedError(id=event_id)

        if event_instance.end_date < datetime.now().date():
            raise EventAlreadyFinishedError(id=event_id)

        data = item.model_dump()
        data["event_id"] = event_id

        instance = await uow.events_applications.create(data=data)

        self._job_scheduler.add_task(send_application_created_email, instance.email, event_instance.name)

        return instance

    async def update_instance(self, id: int, item: EventApplicationUpdateInSchema, uow: GenericUnitOfWork,
                              **kwargs) -> EventApplication:
        instance = await uow.events_applications.retrieve(id=id)

        if not instance:
            raise EventApplicationNotFoundError(id=id)

        event_instance = await uow.events.retrieve(id=instance.event_id)

        if not event_instance:
            raise EventNotFoundError(id=instance.event_id)

        data = item.model_dump()

        updated_instance = await uow.events_applications.update(id=id, data=data)

        if updated_instance.status == EventApplicationStatus.ACCEPTED:
            self._job_scheduler.add_task(send_application_accepted_email, updated_instance.email, event_instance.name)

        if updated_instance.status == EventApplicationStatus.REJECTED:
            self._job_scheduler.add_task(send_application_rejected_email, updated_instance.email, event_instance.name)

        return updated_instance

    async def delete_instance(self, id: int, uow: GenericUnitOfWork, **kwargs):
        instance = await uow.events_applications.retrieve(id=id)

        if not instance:
            raise EventApplicationNotFoundError(id=id)

        await uow.events_applications.delete(id=id)

    async def retrieve_all(self,
                           page: int,
                           per_page: int,
                           uow: GenericUnitOfWork,
                           fio_contains: Optional[str] = None,
                           statuses: Optional[List[int]] = None,
                           event_id: Optional[int] = None, ):
        paginated_model = await self.retrieve_all_instances(page=page,
                                                            per_page=per_page,
                                                            uow=uow,
                                                            fio_contains=fio_contains,
                                                            statuses=statuses,
                                                            event_id=event_id)

        return self.schema_paginated_out.model_validate(asdict(paginated_model))

    async def create(self, event_id: int, item: EventApplicationCreateInSchema, uow: GenericUnitOfWork, **kwargs):
        instance = await self.create_instance(event_id=event_id, item=item, uow=uow)

        return self.schema_create_out.model_validate(instance)
