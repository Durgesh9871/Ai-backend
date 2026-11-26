from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def handle_http_exception(
        _request: Request,
        exception: HTTPException,
    ) -> JSONResponse:
        error_codes = {
            404: "RESOURCE_NOT_FOUND",
            409: "CONFLICT",
            401: "UNAUTHENTICATED",
            403: "FORBIDDEN",
        }

        return JSONResponse(
            status_code=exception.status_code,
            content={
                "error": {
                    "code": error_codes.get(
                        exception.status_code,
                        "REQUEST_FAILED",
                    ),
                    "message": str(exception.detail),
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        _request: Request,
        exception: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": jsonable_encoder(exception.errors()),
                }
            },
        )