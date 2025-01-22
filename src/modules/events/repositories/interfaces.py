from abc import ABC, abstractmethod
from typing import Optional, List

from core.pagination.model import PaginatedModel
from core.repositories.interfaces import IRetrieveMixin, ICreateMixin, IUpdateMixin, IDeleteMixin
from db.sqlalchemy.models import Event, EventApplication


class IEventsRepository(IRetrieveMixin[Event],
                        # IRetrievePageMixin[Event],
                        ICreateMixin[Event],
                        IUpdateMixin[Event],
                        IDeleteMixin,
                        ABC):
    """
    Interface for events repository.
    """

    @abstractmethod
    async def retrieve_all(self, page: int,
                           per_page: int,
                           name_contains: Optional[str] = None,
                           *args,
                           **kwargs) -> PaginatedModel[Event]:
        raise NotImplementedError


class IEventApplicationsRepository(IRetrieveMixin[EventApplication],
                                   # IRetrievePageMixin[Event],
                                   ICreateMixin[EventApplication],
                                   IUpdateMixin[EventApplication],
                                   IDeleteMixin,
                                   ABC):
    """
    Interface for event applications repository.
    """

    @abstractmethod
    async def retrieve_all(self, page: int,
                           per_page: int,
                           fio_contains: Optional[str] = None,
                           event_id: Optional[int] = None,
                           statuses: Optional[List[int]] = None,
                           *args,
                           **kwargs) -> PaginatedModel[EventApplication]:
        raise NotImplementedError
