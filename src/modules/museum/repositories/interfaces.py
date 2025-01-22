from abc import ABC, abstractmethod
from typing import Optional, List

from core.pagination.model import PaginatedModel
from core.repositories.interfaces import IUpdateMixin, ICreateMixin, IDeleteMixin, IRetrieveMixin
from db.sqlalchemy.models import MuseumHall, MuseumSection


class IMuseumHallRepository(ICreateMixin[MuseumHall],
                            IUpdateMixin[MuseumHall],
                            IDeleteMixin,
                            ABC):
    """
    Interface for museum hall repository.
    """

    @abstractmethod
    async def retrieve(self, id: int, include_sections: bool = False) -> Optional[MuseumHall]:
        raise NotImplementedError

    @abstractmethod
    async def retrieve_all(self, page: int, per_page: int, include_sections: bool = False) -> PaginatedModel[MuseumHall]:
        raise NotImplementedError


class IMuseumSectionRepository(IRetrieveMixin[MuseumSection],
                               ICreateMixin[MuseumSection],
                               IUpdateMixin[MuseumSection],
                               IDeleteMixin,
                               ABC):
    """
    Interface for museum section repository.
    """

    @abstractmethod
    async def retrieve_all(self,
                           page: int,
                           per_page: int,
                           hall_id: Optional[int] = None) -> PaginatedModel[MuseumSection]:
        raise NotImplementedError
