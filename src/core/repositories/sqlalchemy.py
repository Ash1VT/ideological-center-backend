from abc import ABC
from typing import Optional, List

from loguru import logger
from sqlalchemy import Select, Insert, insert, Update, update, select, Delete, delete, exists
from sqlalchemy.ext.asyncio import AsyncSession

from core.pagination.model import PaginatedModel
from core.pagination.paginator.sqlalchemy import SQLAlchemyPaginator
from core.repositories.generic import GenericRepository


class SQLAlchemyRepository[Model](GenericRepository, ABC):
    """
    An abstract base class for repository operations using SQLAlchemy.
    """

    model: Model = None

    def __init__(self, session: AsyncSession):
        """
        Initialize a new SQLAlchemyRepository instance.

        Args:
            session (AsyncSession): An asynchronous SQLAlchemy session.
        """

        self._session = session

    def _get_retrieve_stmt(self, id: int, **kwargs) -> Select:
        """
        Create a SELECT statement to retrieve a record by its ID.

        Args:
            id (int): The ID of the record to retrieve.
            **kwargs: Additional keyword arguments.

        Returns:
            Select: The SELECT statement to retrieve the record.
        """

        return select(self.model).where(self.model.id == id)

    def _get_list_stmt(self, **kwargs) -> Select:
        """
        Create a SELECT statement to retrieve a list of records.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            Select: The SELECT statement to retrieve the list of records.
        """

        return select(self.model)

    def _get_create_stmt(self, data: dict, **kwargs) -> Insert:
        """
        Create an INSERT statement to add a new record.

        Args:
            data (dict): A dictionary containing the data for the new record.
            **kwargs: Additional keyword arguments.

        Returns:
            Insert: The INSERT statement to add the new record.
        """

        return insert(self.model).values(**data).returning(self.model)

    def _get_update_stmt(self, id: int, data: dict, **kwargs) -> Update:
        """
        Create an UPDATE statement to modify an existing record by its ID.

        Args:
            id (int): The ID of the record to update.
            data (dict): A dictionary containing the updated data.
            **kwargs: Additional keyword arguments.

        Returns:
            Update: The UPDATE statement to modify the existing record.
        """

        return update(self.model).where(self.model.id == id).values(**data).returning(self.model)

    def _get_delete_stmt(self, id: int, **kwargs) -> Delete:
        """
        Create a DELETE statement to remove a record by its ID.

        Args:
            id (int): The ID of the record to delete.
            **kwargs: Additional keyword arguments.

        Returns:
            Delete: The DELETE statement to remove the record.
        """

        return delete(self.model).where(self.model.id == id)

    def _get_exists_stmt(self, id: int, **kwargs) -> Select:
        """
        Create a SELECT statement to check if a record exists by its ID.

        Args:
            id (int): The ID of the record to check.
            **kwargs: Additional keyword arguments.

        Returns:
            Select: The SELECT statement to check if the record exists.
        """

        stmt = self._get_retrieve_stmt(id, **kwargs)
        return select(exists(stmt))

    async def retrieve(self, id: int, **kwargs) -> Optional[Model]:
        stmt = self._get_retrieve_stmt(id=id, **kwargs)
        result = await self._session.execute(stmt)
        result = result.scalar_one_or_none()

        if result:
            logger.debug(f"Retrieved {self.model.__name__} with id={id}")
            return result

        logger.warning(f"Requested {self.model.__name__} with id={id} but it not found")

    # async def retrieve_all(self, **kwargs) -> List[Model]:
    #     stmt = self._get_list_stmt(**kwargs)
    #     result = await self._session.execute(stmt)
    #     result = [r[0] for r in result.fetchall()]
    #
    #     logger.debug(f"Retrieved list of {self.model.__name__}")
    #
    #     return result

    async def retrieve_all(self, page: int, per_page: int, *args, **kwargs) -> PaginatedModel[Model]:
        paginator = SQLAlchemyPaginator(session=self._session,
                                        query=self._get_list_stmt(**kwargs),
                                        page=page,
                                        per_page=per_page)
        logger.debug(f"Retrieved page {page} of {per_page} of {self.model.__name__}")
        return await paginator.get_response()

    async def create(self, data: dict, **kwargs) -> Model:
        stmt = self._get_create_stmt(data=data, **kwargs)
        result = await self._session.execute(stmt)
        result = result.scalar_one()

        logger.debug(f"Created {self.model.__name__} with id={result.id}")

        return result

    async def update(self, id: int, data: dict, **kwargs) -> Optional[Model]:
        stmt = self._get_update_stmt(id=id, data=data, **kwargs)
        result = await self._session.execute(stmt)
        result = result.scalar_one_or_none()

        if result:
            logger.debug(f"Updated {self.model.__name__} with id={id}")
            return result

        logger.warning(f"Requested to update {self.model.__name__} with id={id} but it not found")

    async def delete(self, id: int, **kwargs):
        stmt = self._get_delete_stmt(id=id, **kwargs)
        await self._session.execute(stmt)
        logger.debug(f"Deleted {self.model.__name__} with id={id}")

    async def exists(self, id: int, **kwargs) -> bool:
        stmt = self._get_exists_stmt(id, **kwargs)
        result = await self._session.execute(stmt)
        result = result.scalar()

        logger.debug(f"Checked for existence {self.model.__name__} with id={id}")

        return result
