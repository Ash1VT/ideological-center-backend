from typing import Any

from core.utils.firebase import upload_image_to_firebase
from db.sqlalchemy.models import MuseumHall, MuseumSection


def upload_museum_hall_image_to_firebase(hall: MuseumHall, image_filename: str, image: Any) -> str:
    return upload_image_to_firebase('IdeologicalCenter/images/museum/halls',
                                    hall.id, hall.image_url,
                                    image_filename,
                                    image)


def upload_museum_section_image_to_firebase(section: MuseumSection, image_filename: str, image: Any) -> str:
    return upload_image_to_firebase('IdeologicalCenter/images/museum/sections',
                                    section.id, section.image_url,
                                    image_filename,
                                    image)
