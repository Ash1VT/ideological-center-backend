from abc import ABC, abstractmethod
from typing import TypeVar, Optional, List

from core.pagination.model import PaginatedModel


class GenericRepository[Model](ABC):
    """
    A generic abstract base class representing a repository interface for database operations.

    This class defines common methods for CRUD (Create, Retrieve, Update, Delete) operations on a database model.
    """

    @abstractmethod
    async def retrieve(self, id: int, *args, **kwargs) -> Optional[Model]:
        """
        Retrieve a record by its ID.

        Args:
            id (int): The ID of the record to retrieve.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Optional[Model]: The retrieved record or None if not found.
        """

        raise NotImplementedError

    # @abstractmethod
    # async def retrieve_all(
    #         self, *args, **kwargs
    # ) -> List[Model]:
    #     """
    #     Retrieve a list of records or None if not found.
    #
    #     Args:
    #         *args: Additional positional arguments.
    #         **kwargs: Additional keyword arguments.
    #
    #     Returns:
    #         List[Model]: List of records.
    #     """
    #
    #     raise NotImplementedError

    @abstractmethod
    async def retrieve_all(self, page: int, per_page: int, *args, **kwargs) -> PaginatedModel:
        """
        Retrieve a page list of records or None if not found.

        Args:
            page (int): The page number.
            per_page (int): The number of records per page.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Paginated data.
        """

        raise NotImplementedError

    @abstractmethod
    async def create(self, data: dict, *args, **kwargs) -> Model:
        """
        Create a new record and return it.

        Args:
            data (dict): A dictionary containing the data for the new record.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Model: The newly created record.
        """

        raise NotImplementedError

    @abstractmethod
    async def update(self, id: int, data: dict, *args, **kwargs) -> Optional[Model]:
        """
        Update an existing record by its ID and return updated record.

        Args:
            id (int): The ID of the record to update.
            data (dict): A dictionary containing the updated data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Optional[Model]: The updated record or None if not found.
        """

        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int, *args, **kwargs):
        """
        Delete a record by its ID and returns it.

        Args:
            id (int): The ID of the record to delete.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """

        raise NotImplementedError

    @abstractmethod
    async def exists(self, id: int, *args, **kwargs) -> bool:
        """
        Check if a record exists by its ID.

        Args:
            id (int): The ID of the record to check.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            bool: True if the record exists, False otherwise.
        """

        raise NotImplementedError
