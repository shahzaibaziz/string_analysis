from fastapi import HTTPException


class InvalidAnalysisOperationError(HTTPException):
    def __init__(self, invalid_option: str, allowed_operations: list[str]) -> None:
        self.invalid_option = invalid_option
        super().__init__(
            status_code=400,
            detail=(
                f"'{invalid_option}' is not a valid operation. "
                f"Allowed operations: {', '.join(allowed_operations)}"
            ),
        )
