import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from exceptions.exception_handlers import register_error_handler
from settings.app import AppConfig
from web.routes import all_routers


def get_application() -> FastAPI:
    application = FastAPI(title=AppConfig.PROJECT_NAME, debug=AppConfig.DEBUG, version=AppConfig.VERSION)

    for router in all_routers:
        application.include_router(router)

    application.add_middleware(
        CORSMiddleware,
        **AppConfig.CORS,
    )

    register_error_handler(application)

    return application


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = get_application()
