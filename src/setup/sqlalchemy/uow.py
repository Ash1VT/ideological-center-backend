from core.uow.sqlalchemy import SqlAlchemyUnitOfWork
from setup.sqlalchemy.session import async_session_maker

__all__ = [
    "get_sqlalchemy_uow",
]


def get_sqlalchemy_uow() -> SqlAlchemyUnitOfWork:
    """
    Gets SqlAlchemyUnitOfWork instance.

    Returns:
        SqlAlchemyOfWork: The instance.
    """

    return SqlAlchemyUnitOfWork(async_session_maker)
