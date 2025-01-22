from typing import Any

from core.utils.firebase import upload_image_to_firebase, upload_file_to_firebase
from db.sqlalchemy.models import Media


def upload_media_image_to_firebase(media: Media, image_filename: str, image: Any) -> str:
    return upload_image_to_firebase('IdeologicalCenter/images/media',
                                    media.id, media.image_url,
                                    image_filename,
                                    image)


def upload_media_photo_to_firebase(media: Media, image_filename: str, image: Any) -> str:
    return upload_image_to_firebase('IdeologicalCenter/images/media/photos',
                                    media.id, media.image_url,
                                    image_filename,
                                    image)


def upload_media_file_to_firebase(media: Media, filename: str, file: Any) -> str:
    return upload_file_to_firebase('IdeologicalCenter/media',
                                   media.id, media.url,
                                   filename,
                                   file)
