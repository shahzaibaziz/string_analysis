from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Human-readable error message")
    status_code: int = Field(..., description="HTTP status code")
    invalid_option: str | None = Field(
        default=None,
        description="The invalid query parameter value, if applicable",
    )
