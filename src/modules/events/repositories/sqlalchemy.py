import datetime
from typing import Optional, List

from loguru import logger
from sqlalchemy import func

from core.pagination.model import PaginatedModel
from core.pagination.paginator.sqlalchemy import SQLAlchemyPaginator
from core.repositories.sqlalchemy import SQLAlchemyRepository
from db.sqlalchemy.models import Event, EventApplication, EventApplicationStatus
from modules.events.repositories.interfaces import IEventsRepository


class SQLAlchemyEventsRepository(SQLAlchemyRepository[Event], IEventsRepository):
    model = Event

    async def retrieve_all(self,
                           page: int,
                           per_page: int,
                           name_contains: Optional[str] = None,
                           start_dt: Optional[datetime.date] = None,
                           end_dt: Optional[datetime.date] = None) -> PaginatedModel[Event]:
        stmt = self._get_list_stmt()

        if name_contains:
            stmt = stmt.where(Event.name.contains(name_contains))

        if start_dt:
            stmt = stmt.where(Event.start_date >= start_dt)

        if end_dt:
            stmt = stmt.where(Event.start_date <= end_dt)

        stmt = stmt.order_by(Event.start_date.desc())

        paginator = SQLAlchemyPaginator(session=self._session,
                                        query=stmt,
                                        page=page,
                                        per_page=per_page)
        logger.debug(f"Retrieved page {page} of {per_page} of {self.model.__name__}")

        return await paginator.get_response()


class SQLAlchemyEventApplicationsRepository(SQLAlchemyRepository[EventApplication], IEventsRepository):
    model = EventApplication

    async def retrieve_all(self, page: int,
                           per_page: int,
                           fio_contains: Optional[str] = None,
                           statuses: Optional[List[int]] = None,
                           event_id: Optional[int] = None) -> PaginatedModel[EventApplication]:
        stmt = self._get_list_stmt()

        if fio_contains:
            stmt = stmt.where(func.lower(EventApplication.fio).like(f'%{fio_contains.lower()}%'))

        if event_id:
            stmt = stmt.where(EventApplication.event_id == event_id)

        if statuses:
            stmt = stmt.where(EventApplication.status.in_([EventApplicationStatus(t) for t in statuses]))

        paginator = SQLAlchemyPaginator(session=self._session,
                                        query=stmt,
                                        page=page,
                                        per_page=per_page)
        logger.debug(f"Retrieved page {page} of {per_page} of {self.model.__name__}")

        return await paginator.get_response()
