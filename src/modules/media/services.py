from dataclasses import asdict
from typing import List, Optional

from fastapi import UploadFile
from loguru import logger

from core.pagination.model import PaginatedModel
from core.pagination.schema import PaginatedOut
from core.services.mixins import DeleteMixin, UpdateMixin, CreateMixin, RetrieveMixin, \
    RetrieveAllMixin
from core.uow.generic import GenericUnitOfWork
from db.sqlalchemy.models import Media, MediaCategory
from db.sqlalchemy.models.media import MediaPhoto, MediaType
from modules.media.errors import MediaNotFoundError, MediaCategoryNotFoundError, MediaTypeNotMatchError, \
    MediaPhotoNotFoundError
from modules.media.schemas import MediaCreateInSchema, MediaRetrieveOutSchema, MediaUpdateInSchema, \
    MediaCreateOutSchema, MediaUpdateOutSchema, MediaCategoryRetrieveOutSchema, MediaCategoryUpdateOutSchema, \
    MediaCategoryCreateOutSchema, MediaCategoryCreateInSchema, MediaCategoryUpdateInSchema, \
    MediaPhotoCreateOutSchema
from modules.media.utils.firebase import upload_media_image_to_firebase, upload_media_file_to_firebase


class MediaService(RetrieveMixin[Media, MediaRetrieveOutSchema],
                   # RetrieveAllMixin[Media, MediaRetrieveOutSchema],
                   CreateMixin[Media, MediaCreateInSchema, MediaCreateOutSchema],
                   UpdateMixin[Media, MediaUpdateInSchema, MediaUpdateOutSchema],
                   DeleteMixin[Media]):
    schema_retrieve_out = MediaRetrieveOutSchema
    schema_paginated_out = PaginatedOut[MediaRetrieveOutSchema]
    schema_create_out = MediaCreateOutSchema
    schema_update_out = MediaUpdateOutSchema

    async def retrieve_instance(self, id: int, uow: GenericUnitOfWork, **kwargs) -> Media:
        instance = await uow.media.retrieve(id=id, include_photos=True)

        if not instance:
            raise MediaNotFoundError(id=id)

        return instance

    async def retrieve_all_instances(self,
                                     page: int,
                                     per_page: int,
                                     uow: GenericUnitOfWork,
                                     name_contains: Optional[str] = None,
                                     types: Optional[List[int]] = None,
                                     category_id: Optional[int] = None,
                                     **kwargs) -> PaginatedModel[Media]:
        return await uow.media.retrieve_all(page=page,
                                            per_page=per_page,
                                            name_contains=name_contains,
                                            types=types,
                                            category_id=category_id,
                                            include_photos=True)

    # async def retrieve_instances_by_category(self,
    #                                          category_id: int,
    #                                          page: int,
    #                                          per_page: int,
    #                                          uow: GenericUnitOfWork, **kwargs) -> PaginatedModel[Media]:
    #     return await uow.media.retrieve_by_category(category_id=category_id, page=page, per_page=per_page,
    #                                                 include_photos=True)

    async def create_instance(self, item: MediaCreateInSchema, uow: GenericUnitOfWork, **kwargs) -> Media:
        # if item.category_id:
        #     media_category = await uow.media_category.retrieve(id=item.category_id)
        #
        #     if not media_category:
        #         raise MediaCategoryNotFoundError(id=item.category_id)

        data = item.model_dump()
        return await uow.media.create(data=data)

    async def update_instance(self, id: int, item: MediaUpdateInSchema, uow: GenericUnitOfWork, **kwargs) -> Media:
        # if item.category_id:
        #     media_category = await uow.media_category.retrieve(id=item.category_id)
        #
        #     if not media_category:
        #         raise MediaCategoryNotFoundError(id=item.category_id)

        data = item.model_dump()
        return await uow.media.update(id=id, data=data)

    async def delete_instance(self, id: int, uow: GenericUnitOfWork, **kwargs):
        instance = await uow.media.retrieve(id=id)

        if not instance:
            raise MediaNotFoundError(id=id)

        await uow.media.delete(id=id)

    async def retrieve_all(self, page: int,
                           per_page: int,
                           uow: GenericUnitOfWork,
                           name_contains: Optional[str] = None,
                           types: Optional[List[int]] = None,
                           category_id: Optional[int] = None) -> PaginatedOut[MediaRetrieveOutSchema]:
        paginated_model = await self.retrieve_all_instances(page=page, per_page=per_page, uow=uow,
                                                            name_contains=name_contains,
                                                            types=types,
                                                            category_id=category_id)

        return self.schema_paginated_out.model_validate(asdict(paginated_model))

    async def upload_image(self, id: int, image: UploadFile, uow: GenericUnitOfWork) -> MediaUpdateOutSchema:
        instance = await uow.media.retrieve(id=id)

        if not instance:
            raise MediaNotFoundError(id=id)

        image_url = upload_media_image_to_firebase(instance, image.filename, image.file)

        updated_instance = await uow.media.update(id, {
            'image_url': image_url
        })

        logger.info(f"Uploaded image for media with id={id}.")

        return self.schema_update_out.model_validate(updated_instance)

    async def upload_file(self, id: int, file: UploadFile, uow: GenericUnitOfWork) -> MediaUpdateOutSchema:
        instance = await uow.media.retrieve(id=id)

        if not instance:
            raise MediaNotFoundError(id=id)

        file_url = upload_media_file_to_firebase(instance, file.filename, file.file)

        updated_instance = await uow.media.update(id, {
            'url': file_url
        })

        logger.info(f"Uploaded file for media with id={id}.")

        return self.schema_update_out.model_validate(updated_instance)


class MediaCategoryService(RetrieveMixin[MediaCategory, MediaCategoryRetrieveOutSchema],
                           # RetrieveAllMixin[MediaCategory, MediaCategoryRetrieveOutSchema],
                           CreateMixin[MediaCategory, MediaCategoryCreateInSchema, MediaCategoryCreateOutSchema],
                           UpdateMixin[MediaCategory, MediaCategoryUpdateInSchema, MediaCategoryUpdateOutSchema],
                           DeleteMixin[MediaCategory]):
    schema_paginated_out = PaginatedOut[MediaCategoryRetrieveOutSchema]
    schema_retrieve_out = MediaCategoryRetrieveOutSchema
    schema_create_out = MediaCategoryCreateOutSchema
    schema_update_out = MediaCategoryUpdateOutSchema

    async def retrieve_instance(self, id: int, uow: GenericUnitOfWork, **kwargs) -> MediaCategory:
        instance = await uow.media_category.retrieve(id=id)

        if not instance:
            raise MediaCategoryNotFoundError(id=id)

        return instance

    async def retrieve_all_instances(self,
                                     page: int,
                                     per_page: int,
                                     uow: GenericUnitOfWork,
                                     types: Optional[List[int]] = None,
                                     **kwargs) -> PaginatedModel[MediaCategory]:
        return await uow.media_category.retrieve_all(page=page, per_page=per_page, types=types)

    async def create_instance(self, item: MediaCategoryCreateInSchema, uow: GenericUnitOfWork,
                              **kwargs) -> MediaCategory:
        data = item.model_dump()
        return await uow.media_category.create(data=data)

    async def update_instance(self, id: int, item: MediaCategoryUpdateInSchema, uow: GenericUnitOfWork,
                              **kwargs) -> MediaCategory:
        data = item.model_dump()
        return await uow.media_category.update(id=id, data=data)

    async def delete_instance(self, id: int, uow: GenericUnitOfWork, **kwargs):
        instance = await uow.media_category.retrieve(id=id)

        if not instance:
            raise MediaCategoryNotFoundError(id=id)

        await uow.media_category.delete(id=id)

    async def retrieve_all(self, page: int,
                           per_page: int,
                           uow: GenericUnitOfWork,
                           types: Optional[List[int]] = None) -> PaginatedOut[MediaCategoryRetrieveOutSchema]:
        paginated_model = await self.retrieve_all_instances(page=page, per_page=per_page, uow=uow, types=types)

        return self.schema_paginated_out.model_validate(asdict(paginated_model))

    async def add_media_to_category(self, category_id: int, media_id: int, uow: GenericUnitOfWork):
        category_instance = await uow.media_category.retrieve(id=category_id)

        if not category_instance:
            raise MediaCategoryNotFoundError(id=category_id)

        media_instance = await uow.media.retrieve(id=media_id)

        if not media_instance:
            raise MediaNotFoundError(id=media_id)

        await uow.media.update(id=media_id, data={'category_id': category_id})

    async def remove_media_from_category(self, category_id: int, media_id: int, uow: GenericUnitOfWork):
        category_instance = await uow.media_category.retrieve(id=category_id)

        if not category_instance:
            raise MediaCategoryNotFoundError(id=category_id)

        media_instance = await uow.media.retrieve(id=media_id)

        if not media_instance:
            raise MediaNotFoundError(id=media_id)

        await uow.media.update(id=media_id, data={'category_id': None})


class MediaPhotoService(DeleteMixin[MediaPhoto]):
    schema_create_out = MediaPhotoCreateOutSchema

    async def create_instance(self, media_id: int, image: UploadFile, uow: GenericUnitOfWork,
                              **kwargs) -> MediaPhoto:
        media_instance = await uow.media.retrieve(id=media_id)

        if not media_instance:
            raise MediaNotFoundError(id=media_id)

        if media_instance.type != MediaType.PHOTO:
            raise MediaTypeNotMatchError()

        # data = item.model_dump()
        instance = await uow.media_photo.create(data={
            'media_id': media_id
        })

        image_url = upload_media_image_to_firebase(instance, image.filename, image.file)

        updated_instance = await uow.media_photo.update(id=instance.id, data={
            'image_url': image_url
        })

        logger.info(f"Created media photo with id={instance.id}.")

        return self.schema_create_out.model_validate(updated_instance)

    async def delete_instance(self, id: int, uow: GenericUnitOfWork, **kwargs):
        instance = await uow.media_photo.retrieve(id=id)

        if not instance:
            raise MediaPhotoNotFoundError(id=id)

        await uow.media_photo.delete(id=id)

    async def create(self, media_id: int,
                     image: UploadFile,
                     uow: GenericUnitOfWork, **kwargs) -> MediaPhotoCreateOutSchema:

        created_instance = await self.create_instance(media_id=media_id, image=image, uow=uow, **kwargs)

        return self.schema_create_out.model_validate(created_instance)
