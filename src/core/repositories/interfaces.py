from abc import ABC, abstractmethod
from typing import Optional, List

from core.pagination.model import PaginatedModel


class IRetrieveMixin[Model](ABC):
    """
    Interface for retrieve mixin.
    """

    @abstractmethod
    async def retrieve(self, id: int) -> Optional[Model]:
        """
        Retrieve a record by its ID.

        Args:
            id (int): The ID of the record to retrieve.

        Returns:
            Optional[Model]: The retrieved record or None if not found.
        """

        raise NotImplementedError


# class IRetrieveAllMixin[Model](ABC):
#     """
#     Interface for retrieve all mixin.
#     """
#
#     @abstractmethod
#     async def retrieve_all(self) -> List[Model]:
#         """
#         Retrieve a list of records.
#
#         Returns:
#             List[Model]: The retrieved list.
#         """
#
#         raise NotImplementedError


class IRetrieveAllMixin[Model](ABC):
    """
    Interface for retrieve all mixin.
    """

    @abstractmethod
    async def retrieve_all(self, page: int, per_page: int, ) -> PaginatedModel[Model]:
        """
        Retrieve a page list of records .

        Args:
            page (int): The page number.
            per_page (int): The number of records per page.

        Returns:
            PaginatedModel[Model]: The retrieved page of records.
        """

        raise NotImplementedError


class ICreateMixin[Model](ABC):
    """
    Interface for create mixin.
    """

    @abstractmethod
    async def create(self, data: dict) -> Model:
        """
        Create a new record and return it.

        Args:
            data (dict): The data to create the record.

        Returns:
            Model: The created record.
        """

        raise NotImplementedError


class IUpdateMixin[Model](ABC):
    """
    Interface for update mixin.
    """

    @abstractmethod
    async def update(self, id: int, data: dict) -> Optional[Model]:
        """
        Update a record by its ID.

        Args:
            id (int): The ID of the record to update.
            data (UpdateModel): The data to update the record.

        Returns:
            Optional[Model]: The updated record or None if not found.
        """

        raise NotImplementedError


class IDeleteMixin(ABC):
    """
    Interface for delete mixin.
    """

    @abstractmethod
    async def delete(self, id: int) -> None:
        """
        Delete a record by its ID.

        Args:
            id (int): The ID of the record to delete.
        """

        raise NotImplementedError
