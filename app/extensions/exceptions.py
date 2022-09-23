from typing import Any
from fastapi import HTTPException, status


class ExtensionNotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: Any = "Extension not found",
    ) -> None:
        super().__init__(status_code, detail)
