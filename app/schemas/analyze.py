from enum import Enum

from pydantic import BaseModel, Field

from app.core.config import settings
from app.schemas.exceptions import InvalidAnalysisOperationError


class AnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=settings.MAX_STRING_LENGTH,
        description="The text to analyze",
    )


class AnalysisOperation(str, Enum):
    word_count = "word_count"
    character_count = "character_count"
    character_count_no_space = "character_count_no_space"
    unique_character_count = "unique_character_count"
    unique_word_count = "unique_word_count"
    sentence_count = "sentence_count"


ALLOWED_OPERATIONS = [operation.value for operation in AnalysisOperation]


class AnalysisResultItem(BaseModel):
    operation: AnalysisOperation = Field(..., description="The analysis operation that was run")
    value: int = Field(..., ge=0, description="The computed result for the operation")


def _parse_operations_query(value: object) -> list[AnalysisOperation] | None:
    if value is None:
        return None

    if isinstance(value, list):
        if not value:
            return None
        if all(isinstance(item, AnalysisOperation) for item in value):
            return list(dict.fromkeys(value))
        value = ",".join(str(item) for item in value)

    if not isinstance(value, str):
        raise ValueError("operations must be a comma-separated list of operation names")

    stripped = value.strip()
    if not stripped:
        return None

    tokens = [token.strip() for token in stripped.split(",") if token.strip()]
    if not tokens:
        return None

    selected: list[AnalysisOperation] = []
    for token in tokens:
        if token not in ALLOWED_OPERATIONS:
            raise InvalidAnalysisOperationError(token, ALLOWED_OPERATIONS)
        selected.append(AnalysisOperation(token))

    return list(dict.fromkeys(selected))
