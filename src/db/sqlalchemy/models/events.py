import enum
from datetime import datetime, date

from sqlalchemy import Column, Integer, String, Date, Enum, case, and_
from sqlalchemy.ext.hybrid import hybrid_property

from db.sqlalchemy.models.base import Base


class EventType(enum.Enum):
    PLANNED = 0
    PASSING = 1
    PASSED = 2


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=True)
    short_description = Column(String(500), nullable=True)
    image_url = Column(String(255), nullable=True)

    location = Column(String(1000), nullable=True)
    participants = Column(String(1000), nullable=True)
    coordinator_contact = Column(String(1000), nullable=True)
    created_at = Column(Date(), default=datetime.now, nullable=False)
    start_date = Column(Date(), nullable=False)
    end_date = Column(Date(), nullable=False)

    @hybrid_property
    def status(self):
        if datetime.now().date() < self.start_date:
            return EventType.PLANNED
        if self.start_date <= datetime.now().date() < self.end_date:
            return EventType.PASSING

        return EventType.PASSED

    @status.expression
    def status(cls):
        return case(
            (datetime.now().date() < cls.start_date, EventType.PLANNED),
            (and_(cls.start_date <= datetime.now().date(), datetime.now().date() < cls.end_date), EventType.PASSING),
            else_=EventType.PASSED,
        )
