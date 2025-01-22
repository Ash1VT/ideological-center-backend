from core.uow.generic import GenericUnitOfWork
from core.uow.transactions import uow_transaction, uow_transaction_with_commit
from setup.settings.app import get_app_settings

__all__ = [
    "get_uow",
    "get_uow_with_commit",
]

settings = get_app_settings()


async def get_uow() -> GenericUnitOfWork:
    """
    Dependency for retrieving the unit of work.

    Yields:
        GenericUnitOfWork: An instance of the GenericUnitOfWork class.
    """

    uow = settings.get_uow()
    async with uow_transaction(uow) as uow:
        yield uow


async def get_uow_with_commit() -> GenericUnitOfWork:
    """
    Dependency for retrieving the unit of work and committing the changes.

    Yields:
        GenericUnitOfWork: An instance of the GenericUnitOfWork class.
    """

    uow = settings.get_uow()
    async with uow_transaction_with_commit(uow) as uow:
        yield uow
