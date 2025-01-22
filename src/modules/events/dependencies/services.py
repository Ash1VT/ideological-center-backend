from fastapi import BackgroundTasks

from modules.events.services import EventService, EventApplicationService


def get_event_service() -> EventService:
    return EventService()


def get_event_application_service(background_tasks: BackgroundTasks) -> EventApplicationService:
    return EventApplicationService(background_tasks=background_tasks)
