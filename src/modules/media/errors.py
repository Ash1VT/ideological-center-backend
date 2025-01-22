from core.errors.base import DatabaseInstanceNotFoundError, AppError
from db.sqlalchemy.models import Media, MediaCategory


class MediaNotFoundError(DatabaseInstanceNotFoundError):

    def __init__(self, id: int):
        super().__init__(field_name="id", field_value=id, model_class=Media)


class MediaCategoryNotFoundError(DatabaseInstanceNotFoundError):

    def __init__(self, id: int):
        super().__init__(field_name="id", field_value=id, model_class=MediaCategory)


class MediaPhotoNotFoundError(DatabaseInstanceNotFoundError):

    def __init__(self, id: int):
        super().__init__(field_name="id", field_value=id, model_class=Media)


class MediaTypeNotMatchError(AppError):

    @property
    def status_code(self) -> int:
        return 400

    @property
    def message(self) -> str:
        return "Media type does not match"
