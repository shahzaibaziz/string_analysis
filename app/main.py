import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.schemas.error import ErrorResponse
from app.schemas.exceptions import InvalidAnalysisOperationError

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(settings.LOG_LEVEL)
    logger.info("Starting %s", settings.APP_NAME)
    app.state.ready = True
    yield
    app.state.ready = False
    logger.info("Shutting down %s", settings.APP_NAME)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        lifespan=lifespan,
    )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                detail="Request validation failed",
                status_code=422,
            ).model_dump(),
        )

    @app.exception_handler(InvalidAnalysisOperationError)
    async def invalid_analysis_operation_handler(
        request: Request, exc: InvalidAnalysisOperationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                detail=str(exc.detail),
                status_code=exc.status_code,
                invalid_option=exc.invalid_option,
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                detail="Internal server error",
                status_code=500,
            ).model_dump(),
        )

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger.info("%s %s", request.method, request.url.path)
        response = await call_next(request)
        logger.info("%s %s -> %d", request.method, request.url.path, response.status_code)
        return response

    app.include_router(health_router)
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()
