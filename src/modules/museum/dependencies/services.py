from modules.museum.services import MuseumSectionService, MuseumHallService


def get_museum_hall_service() -> MuseumHallService:
    return MuseumHallService()


def get_museum_section_service() -> MuseumSectionService:
    return MuseumSectionService()

