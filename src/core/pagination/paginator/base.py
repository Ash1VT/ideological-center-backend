from abc import ABC, abstractmethod
from typing import List

from core.pagination.model import PaginatedModel


class BasePaginator[Model](ABC):
    def __init__(self, page: int = 1, per_page: int = None):
        self._page = page
        self._per_page = per_page
        self._limit = per_page * page if per_page else None
        self._offset = (page - 1) * per_page if per_page else None

    @abstractmethod
    async def get_response(self) -> PaginatedModel[Model]:
        raise NotImplementedError

    @abstractmethod
    async def get_items(self) -> List[Model]:
        raise NotImplementedError

    @abstractmethod
    async def _get_total_count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def _get_total_filtered_count(self) -> int:
        raise NotImplementedError

    def _get_number_of_pages(self, count: int) -> int:
        if not self._per_page:
            return 1

        rest = count % self._per_page
        quotient = count // self._per_page
        return quotient if not rest else quotient + 1
