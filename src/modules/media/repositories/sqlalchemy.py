from typing import Optional, List

from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from core.pagination.model import PaginatedModel
from core.pagination.paginator.sqlalchemy import SQLAlchemyPaginator
from core.repositories.sqlalchemy import SQLAlchemyRepository
from db.sqlalchemy.models import Event, MediaCategory, Media
from db.sqlalchemy.models.media import MediaPhoto, MediaType
from modules.media.repositories.interfaces import IMediaRepository, IMediaCategoryRepository, IMediaPhotoRepository


class SQLAlchemyMediaRepository(SQLAlchemyRepository[Event], IMediaRepository):
    model = Media

    async def retrieve(self, id: int, include_photos: bool = False) -> Optional[Media]:
        stmt = super()._get_retrieve_stmt(id=id)

        if include_photos:
            stmt = stmt.options(selectinload(Media.media_photos))

        result = await self._session.execute(stmt)
        result = result.scalar_one_or_none()

        if result:
            logger.debug(f"Retrieved {self.model.__name__} with id={id}")
            return result

        logger.warning(f"Requested {self.model.__name__} with id={id} but it not found")

    async def retrieve_all(self,
                           page: int,
                           per_page: int,
                           name_contains: Optional[str] = None,
                           types: Optional[List[int]] = None,
                           category_id: Optional[int] = None,
                           include_photos: bool = False) -> PaginatedModel[Media]:
        stmt = super()._get_list_stmt()
        if types:
            stmt = stmt.where(Media.type.in_([MediaType(t) for t in types]))

        if category_id:
            stmt = stmt.join(MediaCategory).where(MediaCategory.id == category_id)

        if include_photos:
            stmt = stmt.options(selectinload(Media.media_photos))

        if name_contains:
            stmt = stmt.where(func.lower(Media.name).like(f'%{name_contains.lower()}%'))

        paginator = SQLAlchemyPaginator(session=self._session,
                                        query=stmt,
                                        page=page,
                                        per_page=per_page)

        logger.debug(f"Retrieved page {page} of {per_page} of {self.model.__name__}")

        return await paginator.get_response()


class SQLAlchemyMediaCategoryRepository(SQLAlchemyRepository[MediaCategory], IMediaCategoryRepository):
    model = MediaCategory

    async def retrieve_all(self,
                           page: int,
                           per_page: int,
                           types: Optional[List[int]] = None) -> PaginatedModel[Media]:
        stmt = super()._get_list_stmt()

        if types:
            stmt = stmt.where(Media.type.in_([MediaType(t) for t in types]))

        paginator = SQLAlchemyPaginator(session=self._session,
                                        query=stmt,
                                        page=page,
                                        per_page=per_page)

        logger.debug(f"Retrieved page {page} of {per_page} of {self.model.__name__}")

        return await paginator.get_response()


class SQLAlchemyMediaPhotoRepository(SQLAlchemyRepository[MediaPhoto], IMediaPhotoRepository):
    model = MediaPhoto
