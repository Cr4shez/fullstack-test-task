from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.api.router import base_router
from src.domain.exceptions import DomainException, FileMissingError

ERROR_MAP = {
    DomainException: status.HTTP_400_BAD_REQUEST,
    FileMissingError: status.HTTP_404_NOT_FOUND,
}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(base_router)


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    status_code = ERROR_MAP.get(type(exc), status.HTTP_400_BAD_REQUEST)

    return JSONResponse(
        status_code=status_code,
        content={"error": exc.__class__.__name__, "message": str(exc)}
    )
