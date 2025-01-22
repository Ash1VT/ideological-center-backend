from modules.media.services import MediaService, MediaCategoryService, MediaPhotoService


def get_media_service() -> MediaService:
    return MediaService()


def get_media_category_service() -> MediaCategoryService:
    return MediaCategoryService()


def get_media_photo_service() -> MediaPhotoService:
    return MediaPhotoService()
