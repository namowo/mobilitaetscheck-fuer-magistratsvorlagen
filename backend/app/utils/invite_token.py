from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

ALGORITHM = "HS256"
TOKEN_TYPE = "invite"


def create_invite_token(
    *,
    email: str,
    gemeinde_id: int,
    rolle_id: int,
    secret: str,
    valid_hours: int,
    is_superuser: bool = False,
    is_local_superuser: bool = False,
) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=valid_hours)
    payload = {
        "email": email,
        "gemeinde_id": gemeinde_id,
        "rolle_id": rolle_id,
        "is_superuser": is_superuser,
        "is_local_superuser": is_local_superuser,
        "exp": expire,
        "type": TOKEN_TYPE,
    }
    return jwt.encode(payload, secret, algorithm=ALGORITHM)


def decode_invite_token(token: str, secret: str) -> dict:
    payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
    if payload.get("type") != TOKEN_TYPE:
        raise JWTError("Invalid token type")
    return payload
