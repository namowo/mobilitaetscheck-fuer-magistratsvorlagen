from typing import Optional

from fastapi import HTTPException, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions as fapi_exceptions
from jose import JWTError
from sqlalchemy.future import select
from uuid import UUID

from app.models.user import User
from app.models.user_rolle import UserRolle
from app.core.config import settings
from app.utils.invite_token import decode_invite_token
from app.services.mail.messages import (
    send_verification,
    send_reset_password,
)

VERWALTUNG_ROLLE_NAME = "Verwaltung"


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET

    async def create(self, user_create, safe=False, request=None):
        session = self.user_db.session

        result = await session.execute(
            select(UserRolle).where(UserRolle.name == VERWALTUNG_ROLLE_NAME)
        )
        verwaltung_rolle = result.scalar_one_or_none()

        gruppe_id = getattr(user_create, "gruppe_id", None)

        token = getattr(user_create, "einladungs_token", None)
        is_verwaltung = verwaltung_rolle and user_create.rolle_id == verwaltung_rolle.id

        if is_verwaltung and not token:
            raise HTTPException(
                status_code=400,
                detail="Verwaltung-Registrierung erfordert einen gültigen Einladungslink.",
            )

        if token:
            try:
                payload = decode_invite_token(token, settings.EINLADUNG_TOKEN_SECRET)
            except JWTError:
                raise HTTPException(
                    status_code=400,
                    detail="Der Einladungslink ist ungültig oder abgelaufen.",
                )
            user_create.gemeinde_id = payload["gemeinde_id"]
            user_create.rolle_id = payload["rolle_id"]
            is_superuser_from_token = payload.get("is_superuser", False)
            is_local_superuser_from_token = payload.get("is_local_superuser", False)

            if is_superuser_from_token or is_local_superuser_from_token:
                if is_superuser_from_token:
                    user_create.is_superuser = True
                if is_local_superuser_from_token:
                    user_create.is_local_superuser = True
                user = await super().create(user_create, safe=False, request=request)
            else:
                user = await super().create(user_create, safe=safe, request=request)
        else:
            user = await super().create(user_create, safe=safe, request=request)

        if gruppe_id is not None:
            db_user = await session.get(User, user.id)
            if db_user:
                db_user.gruppe_id = gruppe_id
                await session.commit()

        return user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")
        try:
            await self.request_verify(user, request)
        except fapi_exceptions.UserAlreadyVerified:
            pass  # Platform Admin is pre-verified, no email needed

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        await send_reset_password(user, token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
        await send_verification(user, token)

    async def on_after_verify(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has been verified")
