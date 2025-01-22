from typing import Optional, List

from pydantic import Field, BaseModel


# MUSEUM SECTION
class MuseumSectionBaseSchema(BaseModel):
    name: str = Field(max_length=255, examples=["Lunch", "Dinner"])
    description: Optional[str] = Field(max_length=255, examples=["Lunch", "Dinner"])


class MuseumSectionRetrieveOutSchema(MuseumSectionBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    hall_id: Optional[int] = Field(ge=0, examples=[1, 2, 3, 4, 5])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class MuseumSectionCreateInSchema(MuseumSectionBaseSchema):
    pass


class MuseumSectionCreateOutSchema(MuseumSectionBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    hall_id: Optional[int] = Field(ge=0, examples=[1, 2, 3, 4, 5])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class MuseumSectionUpdateInSchema(MuseumSectionBaseSchema):
    hall_id: Optional[int] = Field(ge=0, examples=[1, 2, 3, 4, 5])


class MuseumSectionUpdateOutSchema(MuseumSectionBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    hall_id: Optional[int] = Field(ge=0, examples=[1, 2, 3, 4, 5])

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


# MUSEUM HALL

class MuseumHallBaseSchema(BaseModel):
    name: str = Field(max_length=255, examples=["Lunch", "Dinner"])
    description: Optional[str] = Field(max_length=255, examples=["Lunch", "Dinner"])


class MuseumHallRetrieveOutSchema(MuseumHallBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    sections: Optional[List[MuseumSectionRetrieveOutSchema]]

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class MuseumHallCreateInSchema(MuseumHallBaseSchema):
    pass


class MuseumHallCreateOutSchema(MuseumHallBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    # sections: Optional[List[MuseumSectionCreateOutSchema]]

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }


class MuseumHallUpdateInSchema(MuseumHallBaseSchema):
    pass


class MuseumHallUpdateOutSchema(MuseumHallBaseSchema):
    id: int = Field(ge=0, examples=[1, 2, 3, 4, 5])
    image_url: Optional[str] = Field(max_length=255, examples=["https://example.com/image.jpg"])
    # sections: Optional[List[MuseumSectionUpdateOutSchema]]

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }
