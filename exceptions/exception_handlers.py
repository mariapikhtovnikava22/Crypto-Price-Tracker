from fastapi import FastAPI, Request, status
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from exceptions.custom_exceptions import BaseAppError, PriceNotFoundError


def register_error_handler(app: FastAPI):

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=str(exc),
        )

    @app.exception_handler(ResponseValidationError)
    async def response_validation_error_handler(request: Request, exc: ResponseValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(BaseAppError)
    async def base_app_exception_handler(request: Request, exc: BaseAppError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )

    @app.exception_handler(PriceNotFoundError)
    async def price_not_found_handler(request: Request, exc: BaseAppError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )
