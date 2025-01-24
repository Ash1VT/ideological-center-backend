import enum
from typing import Optional, List

from pydantic import Field, BaseModel

from db.sqlalchemy.models import MediaType


# class MediaTypeSchema(enum.Enum):
#     METHOD_DOC = 0
#     NORM_DOC = 1
#     STUDY_MATERIAL = 2
#     IMAGE = 3
#     VIDEO = 4
#     PRESENTATION = 5


# MEDIA PHOTO

class MediaPhotoBaseSchema(BaseModel):
    pass


class MediaPhotoRetrieveOutSchema(MediaPhotoBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    media_id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


# class MediaPhotoCreateInSchema(MediaPhotoBaseSchema):
#     pass


class MediaPhotoCreateOutSchema(MediaPhotoBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


# MEDIA

class MediaBaseSchema(BaseModel):
    name: str = Field(max_length=255, examples=["Lunch", "Dinner"])
    description: Optional[str] = Field(max_length=255, examples=["Lunch", "Dinner"])
    type: MediaType = Field(examples=[MediaType.METHOD_DOC,
                                      MediaType.NORM_DOC,
                                      MediaType.STUDY_MATERIAL,
                                      MediaType.PHOTO,
                                      MediaType.VIDEO,
                                      MediaType.PRESENTATION])


class MediaRetrieveOutSchema(MediaBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    media_photos: Optional[List[MediaPhotoRetrieveOutSchema]]
    category_id: Optional[int] = Field(ge=0, examples=[1, 2, 3, 4, 5], default=None)

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class MediaCreateInSchema(MediaBaseSchema):
    pass


class MediaCreateOutSchema(MediaBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    # media_photos: Optional[List[MediaPhotoCreateOutSchema]]
    category_id: Optional[int] = Field(ge=0, examples=[1, 2, 3, 4, 5], default=None)

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class MediaUpdateInSchema(MediaBaseSchema):
    pass


class MediaUpdateOutSchema(MediaBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    # media_photos: Optional[List[MediaPhotoRetrieveOutSchema]]
    category_id: Optional[int] = Field(ge=0, examples=[1, 2, 3, 4, 5], default=None)

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


# MEDIA CATEGORY
class MediaCategoryBaseSchema(BaseModel):
    name: str = Field(max_length=255, examples=["Lunch", "Dinner"])
    type: MediaType = Field(examples=[MediaType.METHOD_DOC,
                                      MediaType.NORM_DOC,
                                      MediaType.STUDY_MATERIAL,
                                      MediaType.PHOTO,
                                      MediaType.VIDEO,
                                      MediaType.PRESENTATION])


class MediaCategoryRetrieveOutSchema(MediaCategoryBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class MediaCategoryCreateInSchema(MediaCategoryBaseSchema):
    pass


class MediaCategoryCreateOutSchema(MediaCategoryBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class MediaCategoryUpdateInSchema(MediaCategoryBaseSchema):
    pass


class MediaCategoryUpdateOutSchema(MediaCategoryBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }
