from core.errors.base import DatabaseInstanceNotFoundError, AppError
from db.sqlalchemy.models import Event, EventApplication


class EventNotFoundError(DatabaseInstanceNotFoundError):

    def __init__(self, id: int):
        super().__init__(field_name="id", field_value=id, model_class=Event)


class EventAlreadyStartedError(AppError):

    def __init__(self, id: int):
        self._id = id
        super().__init__()

    @property
    def status_code(self) -> int:
        return 400

    @property
    def message(self) -> str:
        return f"Event with id={self._id} already started"


class EventAlreadyFinishedError(AppError):

    def __init__(self, id: int):
        self._id = id
        super().__init__()

    @property
    def status_code(self) -> int:
        return 400

    @property
    def message(self) -> str:
        print(self._id)
        return f"Event with id={self._id} already finished"


class EventApplicationNotFoundError(DatabaseInstanceNotFoundError):

    def __init__(self, id: int):
        super().__init__(field_name="id", field_value=id, model_class=EventApplication)
