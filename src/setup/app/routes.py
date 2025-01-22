from fastapi import APIRouter, FastAPI

from modules.events.api.applications import events_applications_router
from modules.events.api.events import events_router
from modules.media.api.media import media_router
from modules.media.api.media_category import media_category_router
from modules.museum.api.hall import museum_hall_router
from modules.museum.api.section import museum_section_router
from modules.users.api.auth import auth_router


def register_routes(app: FastAPI, api_router: APIRouter) -> None:
    # api_router = APIRouter(prefix="/api/v1")
    api_router.include_router(auth_router)
    api_router.include_router(events_router)
    api_router.include_router(events_applications_router)
    api_router.include_router(media_router)
    api_router.include_router(media_category_router)
    api_router.include_router(museum_hall_router)
    api_router.include_router(museum_section_router)
    app.include_router(api_router)
