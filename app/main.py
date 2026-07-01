from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.health import router as health_router
from app.api.v1.api import api_router
from app.core.config import settings
from app.schemas.error import ErrorResponse
from app.schemas.exceptions import InvalidAnalysisOperationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ready = True
    yield
    app.state.ready = False


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

    app.include_router(health_router)
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()
