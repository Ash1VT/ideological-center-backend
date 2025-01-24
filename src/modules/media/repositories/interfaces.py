from abc import ABC, abstractmethod
from typing import Optional, List

from core.pagination.model import PaginatedModel
from core.repositories.interfaces import IRetrieveMixin, ICreateMixin, IUpdateMixin, IDeleteMixin, \
    IRetrieveAllMixin
from db.sqlalchemy.models import Media, MediaCategory
from db.sqlalchemy.models.media import MediaPhoto


class IMediaRepository(ICreateMixin[Media],
                       IUpdateMixin[Media],
                       IDeleteMixin,
                       ABC):
    """
    Interface for media repository.
    """

    @abstractmethod
    async def retrieve(self, id: int, include_photos: bool = False) -> Optional[Media]:
        raise NotImplementedError

    @abstractmethod
    async def retrieve_all(self,
                           page: int,
                           per_page: int,
                           name_contains: Optional[str] = None,
                           types: Optional[List[int]] = None,
                           category_id: Optional[int] = None,
                           include_photos: bool = False) -> PaginatedModel[Media]:
        raise NotImplementedError


class IMediaCategoryRepository(IRetrieveMixin[MediaCategory],
                               # IRetrieveAllMixin[MediaCategory],
                               ICreateMixin[MediaCategory],
                               IUpdateMixin[MediaCategory],
                               IDeleteMixin,
                               ABC):
    """
    Interface for media category repository.
    """

    @abstractmethod
    async def retrieve_all(self,
                           page: int,
                           per_page: int,
                           types: Optional[List[int]] = None) -> PaginatedModel[Media]:
        raise NotImplementedError


class IMediaPhotoRepository(IRetrieveMixin[MediaPhoto],
                            ICreateMixin[MediaPhoto],
                            IUpdateMixin[MediaPhoto],
                            IDeleteMixin,
                            ABC):
    """
    Interface for media photo repository.
    """

    pass
