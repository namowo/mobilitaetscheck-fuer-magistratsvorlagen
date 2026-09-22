from typing import AsyncGenerator, Optional

from fastapi import Depends, Header, HTTPException, status
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.config import settings
from app.core.db import async_session_maker
from app.models.user import User
from app.services.user.user_manager import UserManager


# Asynchronous Database Dependencies
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


cookie_transport = CookieTransport(
    cookie_samesite=None,
    cookie_httponly=True,
    cookie_secure=True,
    cookie_max_age=settings.JWT_LIFETIME_SECONDS,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.JWT_SECRET_KEY, lifetime_seconds=settings.JWT_LIFETIME_SECONDS
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# FastAPI Users Dependencies
fastapi_users = FastAPIUsers[User, UUID](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(superuser=True)

ADMIN_ROLLE_NAME = "Admin"
VERWALTUNG_ROLLE_NAME = "Verwaltung"


async def current_platform_admin(user: User = Depends(current_active_user)) -> User:
    if not user.is_superuser or user.rolle.name != ADMIN_ROLLE_NAME:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Keine Berechtigung")
    return user


async def current_gemeinde_admin(user: User = Depends(current_active_user)) -> User:
    if not user.is_local_superuser or user.rolle.name != VERWALTUNG_ROLLE_NAME:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Keine Berechtigung")
    return user


POLITIK_ROLLE_NAME = "Politik"

# Roles a Platform Admin may demo the read-scoping of. This is a
# view/authorship-attribution hint only — it never grants any permission
# beyond what the real account already has, and is ignored for anyone who
# isn't a genuine Platform Admin (user.is_superuser + Admin role).
VIEW_AS_ROLLEN = {VERWALTUNG_ROLLE_NAME, POLITIK_ROLLE_NAME}


async def get_effective_is_politik(
    user: User = Depends(current_active_user),
    x_view_as_rolle: Optional[str] = Header(None),
) -> bool:
    """
    Whether the request should be treated as coming from a Politik user for
    read-scoping and content-authorship purposes.

    For a real Politik user this always mirrors their actual role. For a
    genuine Platform Admin (is_superuser + Admin role), the optional
    X-View-As-Rolle header lets them narrow their own view to demo what a
    Politik/Verwaltung user would see — it can only ever restrict what the
    request returns, never widen it, and is ignored for every other account.
    """
    is_real_politik = not user.is_superuser and user.rolle.name == POLITIK_ROLLE_NAME
    if is_real_politik:
        return True

    is_platform_admin = user.is_superuser and user.rolle.name == ADMIN_ROLLE_NAME
    if is_platform_admin and x_view_as_rolle in VIEW_AS_ROLLEN:
        return x_view_as_rolle == POLITIK_ROLLE_NAME

    return False
