import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.analyze import ALLOWED_OPERATIONS, AnalysisOperation, _parse_operations_query
from app.schemas.exceptions import InvalidAnalysisOperationError

client = TestClient(app)


def test_analyze_runs_all_operations_by_default():
    response = client.post("/v1/analyze", json={"text": "hello world"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == len(AnalysisOperation)
    assert {item["operation"] for item in body} == set(ALLOWED_OPERATIONS)


def test_analyze_runs_selected_comma_separated_operations():
    response = client.post(
        "/v1/analyze",
        json={"text": "hello world"},
        params={"operations": "word_count,character_count"},
    )

    assert response.status_code == 200
    assert response.json() == [
        {"operation": "word_count", "value": 2},
        {"operation": "character_count", "value": 11},
    ]


def test_analyze_rejects_invalid_operation():
    response = client.post(
        "/v1/analyze",
        json={"text": "hello"},
        params={"operations": "bad_op"},
    )

    assert response.status_code == 400
    body = response.json()
    assert body["status_code"] == 400
    assert body["invalid_option"] == "bad_op"
    assert "Allowed operations:" in body["detail"]
    for operation in ALLOWED_OPERATIONS:
        assert operation in body["detail"]


def test_analyze_rejects_empty_text():
    response = client.post("/v1/analyze", json={"text": ""})

    assert response.status_code == 422
    assert response.json()["detail"] == "Request validation failed"


def test_analyze_rejects_text_over_max_length():
    response = client.post("/v1/analyze", json={"text": "x" * 101})

    assert response.status_code == 422
    assert response.json()["detail"] == "Request validation failed"


def test_parse_operations_query_returns_none_for_missing_value():
    assert _parse_operations_query(None) is None


def test_parse_operations_query_parses_comma_separated_values():
    result = _parse_operations_query("word_count, character_count ,word_count")

    assert result == [AnalysisOperation.word_count, AnalysisOperation.character_count]


def test_parse_operations_query_raises_for_invalid_token():
    with pytest.raises(InvalidAnalysisOperationError) as exc_info:
        _parse_operations_query("word_count,invalid_op")

    assert exc_info.value.invalid_option == "invalid_op"
