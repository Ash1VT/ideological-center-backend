from core.errors.base import DatabaseInstanceNotFoundError
from db.sqlalchemy.models import MuseumHall, MuseumSection


class MuseumHallNotFoundError(DatabaseInstanceNotFoundError):

    def __init__(self, id: int):
        super().__init__(field_name="id", field_value=id, model_class=MuseumHall)


class MuseumSectionNotFoundError(DatabaseInstanceNotFoundError):

    def __init__(self, id: int):
        super().__init__(field_name="id", field_value=id, model_class=MuseumSection)
