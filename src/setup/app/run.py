from fastapi import FastAPI

from setup.settings.server import get_server_settings


def start_app(app: FastAPI | str) -> None:
    import uvicorn

    settings = get_server_settings()
    uvicorn.run(
        app,
        host=settings.web_app_host,
        port=settings.web_app_port,
        reload=settings.reload,
    )
