from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.sqlalchemy.models.base import Base


class MuseumHall(Base):
    __tablename__ = "museum_hall"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    image_url = Column(String(255), nullable=True)

    sections = relationship("MuseumSection",
                            cascade="all, delete-orphan",
                            uselist=True)


class MuseumSection(Base):
    __tablename__ = "museum_section"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

    image_url = Column(String(255), nullable=True)

    hall_id = Column(
        Integer,
        ForeignKey("museum_hall.id", name="fk_museum_section_hall", ondelete="CASCADE"),
        nullable=False,
    )
