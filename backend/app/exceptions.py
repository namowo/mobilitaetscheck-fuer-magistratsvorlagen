from fastapi import Request
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse

from app.crud.exceptions import AuthorizationError, DatabaseCommitError, NotFoundError


async def authorization_exception_handler(request: Request, exc: AuthorizationError):
    return JSONResponse(status_code=403, content={"message": exc.message})


async def database_commit_exception_handler(request: Request, exc: DatabaseCommitError):
    original = exc.original_exception
    if isinstance(original, IntegrityError) and getattr(
        original.orig, "sqlstate", None
    ) == "23505":
        return JSONResponse(
            status_code=409,
            content={
                "message": "Ein Eintrag mit diesen Werten existiert bereits.",
                "detail": "duplicate",
            },
        )
    return JSONResponse(status_code=500, content={"message": exc.message})


async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"message": exc.message})
