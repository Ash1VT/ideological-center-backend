from typing import Optional, List

from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.pagination.model import PaginatedModel
from core.pagination.paginator.sqlalchemy import SQLAlchemyPaginator
from core.repositories.sqlalchemy import SQLAlchemyRepository
from db.sqlalchemy.models import MuseumHall, MuseumSection
from modules.museum.repositories.interfaces import IMuseumHallRepository, IMuseumSectionRepository


class SQLAlchemyMuseumHallRepository(SQLAlchemyRepository[MuseumHall], IMuseumHallRepository):
    model = MuseumHall

    async def retrieve(self, id: int, include_sections: bool = False) -> Optional[MuseumHall]:
        stmt = super()._get_retrieve_stmt(id=id)

        if include_sections:
            stmt = stmt.options(selectinload(MuseumHall.sections))

        result = await self._session.execute(stmt)
        result = result.scalar_one_or_none()

        if result:
            logger.debug(f"Retrieved {self.model.__name__} with id={id}")
            return result

        logger.warning(f"Requested {self.model.__name__} with id={id} but it not found")

    async def retrieve_all(self, page: int, per_page: int, include_sections: bool = False) -> PaginatedModel[MuseumHall]:
        stmt = super()._get_list_stmt()

        if include_sections:
            stmt = stmt.options(selectinload(MuseumHall.sections))

        paginator = SQLAlchemyPaginator(session=self._session,
                                        query=stmt,
                                        page=page,
                                        per_page=per_page)

        logger.debug(f"Retrieved page {page} of {per_page} of {self.model.__name__}")

        return await paginator.get_response()


class SQLAlchemyMuseumSectionRepository(SQLAlchemyRepository[MuseumSection], IMuseumSectionRepository):
    model = MuseumSection

    async def retrieve_all(self, page: int, per_page: int, hall_id: Optional[int] = None) -> PaginatedModel[MuseumSection]:
        stmt = super()._get_list_stmt()

        if hall_id:
            stmt = stmt.where(MuseumSection.hall_id == hall_id)

        paginator = SQLAlchemyPaginator(session=self._session,
                                        query=stmt,
                                        page=page,
                                        per_page=per_page)
        logger.debug(f"Retrieved page {page} of {per_page} of {self.model.__name__}")

        return await paginator.get_response()
