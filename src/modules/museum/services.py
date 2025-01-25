from dataclasses import asdict
from typing import Optional

from fastapi import UploadFile
from loguru import logger

from core.pagination.model import PaginatedModel
from core.pagination.schema import PaginatedOut
from core.services.mixins import RetrieveMixin, CreateMixin, UpdateMixin, DeleteMixin, RetrieveAllMixin
from core.uow.generic import GenericUnitOfWork
from db.sqlalchemy.models import MuseumHall, MuseumSection
from modules.museum.errors import MuseumHallNotFoundError, MuseumSectionNotFoundError
from modules.museum.schemas import MuseumHallUpdateInSchema, MuseumHallCreateInSchema, MuseumHallRetrieveOutSchema, \
    MuseumHallCreateOutSchema, MuseumHallUpdateOutSchema, MuseumSectionUpdateOutSchema, MuseumSectionCreateOutSchema, \
    MuseumSectionRetrieveOutSchema, MuseumSectionCreateInSchema, MuseumSectionUpdateInSchema
from modules.museum.utils.firebase import upload_museum_hall_image_to_firebase, upload_museum_section_image_to_firebase


class MuseumHallService(RetrieveMixin[MuseumHall, MuseumHallRetrieveOutSchema],
                        CreateMixin[MuseumHall, MuseumHallCreateInSchema, MuseumHallCreateOutSchema],
                        UpdateMixin[MuseumHall, MuseumHallUpdateInSchema, MuseumHallUpdateOutSchema],
                        DeleteMixin[MuseumHall]):
    schema_paginated_out = PaginatedOut[MuseumHallRetrieveOutSchema]
    schema_retrieve_out = MuseumHallRetrieveOutSchema
    schema_create_out = MuseumHallCreateOutSchema
    schema_update_out = MuseumHallUpdateOutSchema

    async def retrieve_instance(self, id: int, uow: GenericUnitOfWork, **kwargs) -> MuseumHall:
        instance = await uow.museum_hall.retrieve(id=id, include_sections=True)

        if not instance:
            raise MuseumHallNotFoundError(id=id)

        return instance

    async def retrieve_all_instances(self,
                                     uow: GenericUnitOfWork,
                                     page: int,
                                     per_page: int,
                                     **kwargs) -> PaginatedModel[MuseumHall]:
        return await uow.museum_hall.retrieve_all(page=page, per_page=per_page, include_sections=True)

    async def create_instance(self, item: MuseumHallCreateInSchema, uow: GenericUnitOfWork, **kwargs) -> MuseumHall:
        data = item.model_dump()
        return await uow.museum_hall.create(data=data)

    async def update_instance(self, id: int, item: MuseumHallUpdateInSchema, uow: GenericUnitOfWork,
                              **kwargs) -> MuseumHall:
        instance = await uow.museum_hall.retrieve(id=id)

        if not instance:
            raise MuseumHallNotFoundError(id=id)

        data = item.model_dump()
        return await uow.museum_hall.update(id=id, data=data)

    async def delete_instance(self, id: int, uow: GenericUnitOfWork, **kwargs):
        instance = await uow.museum_hall.retrieve(id=id)

        if not instance:
            raise MuseumHallNotFoundError(id=id)

        await uow.museum_hall.delete(id=id)

    async def retrieve_all(self,
                           uow: GenericUnitOfWork,
                           page: int,
                           per_page: int,
                           **kwargs) -> PaginatedOut[MuseumHallRetrieveOutSchema]:
        paginated_model = await self.retrieve_all_instances(uow=uow, page=page, per_page=per_page, **kwargs)
        return self.schema_paginated_out.model_validate(asdict(paginated_model))

    async def upload_image(self, id: int, image: UploadFile, uow: GenericUnitOfWork,
                           **kwargs) -> MuseumHallUpdateOutSchema:
        instance = await uow.museum_hall.retrieve(id=id)

        if not instance:
            raise MuseumHallNotFoundError(id=id)

        image_url = upload_museum_hall_image_to_firebase(instance, image.filename, image.file)

        updated_instance = await uow.museum_hall.update(id, {
            'image_url': image_url
        })

        logger.info(f"Uploaded image for museum hall with id={id}.")

        return self.schema_update_out.model_validate(updated_instance)


class MuseumSectionService(RetrieveMixin[MuseumSection, MuseumSectionRetrieveOutSchema],
                           # CreateMixin[MuseumSection, MuseumSectionCreateInSchema, MuseumSectionCreateOutSchema],
                           UpdateMixin[MuseumSection, MuseumSectionUpdateInSchema, MuseumSectionUpdateOutSchema],
                           DeleteMixin[MuseumSection]):
    schema_paginated_out = PaginatedOut[MuseumSectionRetrieveOutSchema]
    schema_retrieve_out = MuseumSectionRetrieveOutSchema
    schema_create_out = MuseumSectionCreateOutSchema
    schema_update_out = MuseumSectionUpdateOutSchema

    async def retrieve_instance(self, id: int, uow: GenericUnitOfWork, **kwargs) -> MuseumSection:
        instance = await uow.museum_section.retrieve(id=id)

        if not instance:
            raise MuseumSectionNotFoundError(id=id)

        return instance

    async def retrieve_all_instances(self,
                                     uow: GenericUnitOfWork,
                                     page: int,
                                     per_page: int,
                                     hall_id: Optional[int] = None,
                                     **kwargs) -> PaginatedModel[MuseumSectionRetrieveOutSchema]:
        if hall_id:
            hall_instance = await uow.museum_hall.retrieve(id=hall_id)

            if not hall_instance:
                raise MuseumHallNotFoundError(id=hall_id)

        return await uow.museum_section.retrieve_all(page=page, per_page=per_page, hall_id=hall_id)

    async def create_instance(self,
                              hall_id: int,
                              item: MuseumSectionCreateInSchema, uow: GenericUnitOfWork,
                              **kwargs) -> MuseumSection:
        hall_instance = await uow.museum_hall.retrieve(id=hall_id)

        if not hall_instance:
            raise MuseumHallNotFoundError(id=hall_id)

        data = item.model_dump()
        data['hall_id'] = hall_id
        return await uow.museum_section.create(data=data)

    async def update_instance(self, id: int, item: MuseumSectionUpdateInSchema, uow: GenericUnitOfWork,
                              **kwargs) -> MuseumSection:
        instance = await uow.museum_section.retrieve(id=id)

        if not instance:
            raise MuseumSectionNotFoundError(id=id)

        # hall_instance = await uow.museum_hall.retrieve(id=item.hall_id)
        #
        # if not hall_instance:
        #     raise MuseumHallNotFoundError(id=item.hall_id)

        data = item.model_dump()
        return await uow.museum_section.update(id=id, data=data)

    async def delete_instance(self, id: int, uow: GenericUnitOfWork, **kwargs):
        instance = await uow.museum_section.retrieve(id=id)

        if not instance:
            raise MuseumSectionNotFoundError(id=id)

        await uow.museum_section.delete(id=id)

    async def retrieve_all(self,
                           uow: GenericUnitOfWork,
                           page: int,
                           per_page: int,
                           hall_id: Optional[int] = None,
                           **kwargs) -> PaginatedOut[MuseumSectionRetrieveOutSchema]:
        paginated_model = await self.retrieve_all_instances(uow=uow, page=page, per_page=per_page, hall_id=hall_id,
                                                            **kwargs)
        return self.schema_paginated_out.model_validate(asdict(paginated_model))

    async def create(self,
                     hall_id: int,
                     item: MuseumSectionCreateInSchema,
                     uow: GenericUnitOfWork,
                     **kwargs):
        instance = await self.create_instance(hall_id, item, uow, **kwargs)
        return self.schema_create_out.model_validate(instance)

    async def upload_image(self, id: int, image: UploadFile, uow: GenericUnitOfWork, ):
        instance = await uow.museum_section.retrieve(id=id)

        if not instance:
            raise MuseumSectionNotFoundError(id=id)

        image_url = upload_museum_section_image_to_firebase(instance, image.filename, image.file)

        updated_instance = await uow.museum_section.update(id, {
            'image_url': image_url
        })

        logger.info(f"Uploaded image for museum section with id={id}.")

        return self.schema_update_out.model_validate(updated_instance)
