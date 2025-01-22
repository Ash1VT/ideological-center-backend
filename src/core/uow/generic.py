from abc import ABC, abstractmethod

from modules.events.repositories.interfaces import IEventsRepository, IEventApplicationsRepository
from modules.media.repositories.interfaces import IMediaRepository, IMediaCategoryRepository, IMediaPhotoRepository
from modules.museum.repositories.interfaces import IMuseumSectionRepository, IMuseumHallRepository


class GenericUnitOfWork(ABC):
    """
    Abstract base class for a generic unit of work (UOW) context manager.

    This class defines the basic structure of a unit of work context manager. Subclasses should implement the
    `commit` and `rollback` methods to provide transaction control logic specific to the data store.
    """

    museum_hall: IMuseumHallRepository = None
    museum_section: IMuseumSectionRepository = None
    media: IMediaRepository = None
    media_category: IMediaCategoryRepository = None
    media_photo: IMediaPhotoRepository = None
    events: IEventsRepository = None
    events_applications: IEventApplicationsRepository = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        """
        Commit the transaction.

        This method should be implemented to commit the changes made during the transaction.
        """

        raise NotImplementedError()

    @abstractmethod
    async def rollback(self):
        """
        Rollback the transaction.

        This method should be implemented to roll back any changes made during the transaction.
        """

        raise NotImplementedError()
