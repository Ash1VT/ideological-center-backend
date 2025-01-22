from fastapi import FastAPI, APIRouter

from setup.app.cores import register_cors
from setup.app.lifespan import lifespan
from setup.app.routes import register_routes
from setup.app.run import start_app
from setup.settings.app import get_app_settings

app = FastAPI(title="Resource Center", lifespan=lifespan)
api_router = APIRouter(prefix="/api/v1")
settings = get_app_settings()

register_cors(app, settings.cors_origins)
register_routes(app, api_router)


if __name__ == "__main__":
    start_app("main:app")
