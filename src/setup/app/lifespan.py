from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from setup.settings.app import get_app_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_app_settings()
    try:
        from setup.firebase import init_firebase
        init_firebase(settings.firebase_storage_bucket)
        logger.info("Firebase initialized")
    except Exception as e:
        logger.error(f"Error initializing firebase: {e}")

    yield

    logger.info("Shutting down...")
