from typing import List

from sqlalchemy import Select, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.pagination.model import PaginatedModel
from core.pagination.paginator.base import BasePaginator


class SQLAlchemyPaginator[Model](BasePaginator):

    def __init__(self, session: AsyncSession, query: Select, page: int = 1, per_page: int = None):
        super().__init__(page, per_page)
        self._session = session
        self._query = query

    async def get_response(self) -> PaginatedModel[Model]:
        total_count = await self._get_total_count()

        return PaginatedModel[Model](
            page=self._page if self._page else 1,
            per_page=self._per_page if self._per_page else total_count,
            number_of_pages=self._get_number_of_pages(total_count),
            total_count=total_count,
            items=await self.get_items(),
        )

    async def get_items(self) -> List[Model]:
        return [instance for instance in await self._session.scalars(self._query.limit(self._limit).offset(self._offset))]

    async def _get_total_count(self) -> int:
        return await self._session.scalar(select(func.count()).select_from(self._query.subquery()))
