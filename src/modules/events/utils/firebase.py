from typing import Any

from core.utils.firebase import upload_image_to_firebase
from db.sqlalchemy.models import Event


def upload_event_image_to_firebase(event: Event, image_filename: str, image: Any) -> str:
    return upload_image_to_firebase('IdeologicalCenter/images/events',
                                    event.id, event.image_url,
                                    image_filename,
                                    image)
