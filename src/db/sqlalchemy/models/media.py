import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from db.sqlalchemy.models.base import Base


class MediaType(enum.IntEnum):
    METHOD_DOC = 0
    NORM_DOC = 1
    STUDY_MATERIAL = 2
    PHOTO = 3
    VIDEO = 4
    PRESENTATION = 5


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)

    name = Column(String(500), nullable=False)
    description = Column(String(2000), nullable=True)

    image_url = Column(String(255), nullable=True)

    url = Column(String(255), nullable=True)

    type = Column(Enum(MediaType), nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("media_category.id", name="fk_media_category", ondelete="SET NULL"),
        nullable=True,
    )

    category = relationship("MediaCategory",
                            back_populates='media',
                            cascade="all, delete",
                            uselist=False)

    media_photos = relationship("MediaPhoto",
                                cascade="all, delete-orphan",
                                uselist=True)


class MediaCategory(Base):
    __tablename__ = "media_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(Enum(MediaType), nullable=False)

    media = relationship("Media",
                         cascade="all, delete",
                         uselist=True,
                         passive_deletes=True)


class MediaPhoto(Base):
    __tablename__ = "media_photo"

    id = Column(Integer, primary_key=True)
    image_url = Column(String(255), nullable=True)

    media_id = Column(
        Integer,
        ForeignKey("media.id", name="fk_media_photo_media", ondelete="CASCADE"),
        nullable=False,
    )
