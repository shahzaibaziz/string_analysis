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


def _tokenize(raw_value: str) -> list[str]:
    return [token.strip() for token in raw_value.split(",") if token.strip()]


def _validate_token(token: str) -> AnalysisOperation:
    if token not in ALLOWED_OPERATIONS:
        raise InvalidAnalysisOperationError(token, ALLOWED_OPERATIONS)
    return AnalysisOperation(token)


def _parse_operations_query(value: str | None) -> list[AnalysisOperation] | None:
    if value is None or not value.strip():
        return None

    tokens = _tokenize(value)
    if not tokens:
        return None

    operations = [_validate_token(token) for token in tokens]
    return list(dict.fromkeys(operations))
