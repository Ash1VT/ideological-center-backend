import enum
from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel, ConfigDict

from db.sqlalchemy.models import EventType, EventApplicationStatus


# EVENTS
class EventBaseSchema(BaseModel):
    name: str = Field(max_length=255, examples=["Lunch", "Dinner"])
    description: Optional[str] = Field(max_length=255, examples=["Lunch", "Dinner"], default=None)
    short_description: Optional[str] = Field(max_length=255, examples=["Lunch", "Dinner"], default=None)
    location: Optional[str] = Field(max_length=255, examples=["123 Main St, Anytown, USA"], default=None)
    participants: Optional[str] = Field(max_length=255, examples=["John Doe, Bill Clinton"], default=None)
    coordinator_contact: Optional[str] = Field(max_length=255, examples=["John Doe, Bill Clinton"], default=None)

    start_date: datetime = Field(examples=[datetime.now()])
    end_date: datetime = Field(examples=[datetime.now()])


class EventRetrieveOutSchema(EventBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"], default=None)
    created_at: datetime = Field(examples=[datetime.now()])
    status: EventType = Field(examples=[EventType.PLANNED,
                                        EventType.PASSING,
                                        EventType.PASSED])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class EventCreateInSchema(EventBaseSchema):
    pass


class EventCreateOutSchema(EventBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"], default=None)
    created_at: datetime = Field(examples=[datetime.now()])
    status: EventType = Field(examples=[EventType.PLANNED,
                                        EventType.PASSING,
                                        EventType.PASSED])
    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class EventUpdateInSchema(EventBaseSchema):
    pass


class EventUpdateOutSchema(EventBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"], default=None)
    created_at: datetime = Field(examples=[datetime.now()])
    status: EventType = Field(examples=[EventType.PLANNED,
                                        EventType.PASSING,
                                        EventType.PASSED])
    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


# EVENT APPLICATIONS

class EventApplicationBaseSchema(BaseModel):
    fio: str = Field(max_length=255, examples=["John Doe, Bill Clinton"])
    email: str = Field(max_length=255, examples=["Lunch", "Dinner"])
    phone: str = Field(max_length=255, examples=["Lunch", "Dinner"])
    comment: Optional[str] = Field(max_length=255, examples=["Lunch", "Dinner"], default=None)
    birthdate: datetime = Field(examples=[datetime.now()])
    study_organisation: str = Field(max_length=255, examples=["Lunch", "Dinner"])


class EventApplicationRetrieveOutSchema(EventApplicationBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    event_id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    status: EventApplicationStatus = Field(examples=[EventApplicationStatus.PENDING])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class EventApplicationCreateInSchema(EventApplicationBaseSchema):
    pass


class EventApplicationCreateOutSchema(EventApplicationBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    event_id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    status: EventApplicationStatus = Field(examples=[EventApplicationStatus.PENDING])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class EventApplicationUpdateInSchema(EventApplicationBaseSchema):
    status: EventApplicationStatus = Field(examples=[EventApplicationStatus.PENDING])


class EventApplicationUpdateOutSchema(EventApplicationBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    event_id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    status: EventApplicationStatus = Field(examples=[EventApplicationStatus.PENDING])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }
