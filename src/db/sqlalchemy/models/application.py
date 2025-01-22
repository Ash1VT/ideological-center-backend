import enum

from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum

from db.sqlalchemy.models.base import Base


class EventApplicationStatus(enum.IntEnum):
    ACCEPTED = 0
    REJECTED = 1
    PENDING = 2


class EventApplication(Base):
    __tablename__ = "events_applications"

    id = Column(Integer, primary_key=True)

    fio = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    birthdate = Column(Date(), nullable=False)
    comment = Column(String(255), nullable=True)
    study_organisation = Column(String(255), nullable=False)

    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(EventApplicationStatus), nullable=False, default=EventApplicationStatus.PENDING)
