from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.schemas.analyze import (
    AnalysisOperation,
    AnalysisResultItem,
    AnalyzeRequest,
    _parse_operations_query,
)
from app.schemas.error import ErrorResponse

router = APIRouter()

OperationsQuery = Annotated[
    str | None,
    Query(
        description=(
            "Comma-separated analysis operations to run. Omit to run all operations. "
            "Example: ?operations=word_count,character_count,character_count_no_space"
        ),
    ),
]


def get_operations(operations: OperationsQuery = None) -> list[AnalysisOperation] | None:
    return _parse_operations_query(operations)


def _resolve_operations(
    operations: list[AnalysisOperation] | None,
) -> list[AnalysisOperation]:
    if not operations:
        return list(AnalysisOperation)
    return list(dict.fromkeys(operations))


def _compute_value(text: str, operation: AnalysisOperation) -> int:
    if operation == AnalysisOperation.word_count:
        return len(text.split())
    if operation == AnalysisOperation.character_count:
        return len(text)
    if operation == AnalysisOperation.character_count_no_space:
        return len(text.replace(" ", ""))
    if operation == AnalysisOperation.unique_character_count:
        return len(set(text))
    if operation == AnalysisOperation.unique_word_count:
        return len(set(text.split()))
    if operation == AnalysisOperation.sentence_count:
        return text.count(".") + text.count("!") + text.count("?")
    raise ValueError(f"Unsupported operation: {operation}")


@router.post(
    "/analyze",
    response_model=list[AnalysisResultItem],
    responses={
        400: {"model": ErrorResponse, "description": "Invalid operations query parameter"},
        422: {"model": ErrorResponse, "description": "Request validation failed"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def analyze_text(
    payload: AnalyzeRequest,
    operations: Annotated[list[AnalysisOperation] | None, Depends(get_operations)] = None,
) -> list[AnalysisResultItem]:
    selected = _resolve_operations(operations)
    return [
        AnalysisResultItem(operation=operation, value=_compute_value(payload.text, operation))
        for operation in selected
    ]
