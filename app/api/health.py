from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter(tags=["health"])


@router.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready", include_in_schema=False, response_model=None)
async def ready(request: Request):
    if getattr(request.app.state, "ready", False):
        return {"status": "ready"}
    return JSONResponse(status_code=503, content={"status": "not ready"})


@router.get("/metrics", include_in_schema=False)
async def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
