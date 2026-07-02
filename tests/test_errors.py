from fastapi.testclient import TestClient

from app.main import create_app


def test_unhandled_exception_returns_500():
    app = create_app()

    @app.get("/trigger-500")
    async def trigger():
        raise RuntimeError("unexpected failure")

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/trigger-500")

    assert response.status_code == 500
    body = response.json()
    assert body["detail"] == "Internal server error"
    assert body["status_code"] == 500
