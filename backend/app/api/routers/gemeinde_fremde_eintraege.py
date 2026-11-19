from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import current_active_user, get_async_session
from app.models.gemeinde import Gemeinde
from app.models.user import User
from app.schemas.gemeinde import (
    GemeindeFremdeEintraegeRead as ReadSchema,
    GemeindeFremdeEintraegeUpdate as UpdateSchema,
)

router = APIRouter()


async def current_einstellungs_editor(user: User = Depends(current_active_user)) -> User:
    """Only kommunale Administrator:innen (local superusers) may change these settings."""
    if not user.is_local_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Keine Berechtigung")
    return user


@router.get("", response_model=ReadSchema)
async def get_fremde_eintraege(user: User = Depends(current_active_user)):
    """Ob Tags, Indikatoren und Textbausteine anderer Kommunen angezeigt werden."""
    return user.gemeinde


@router.patch("", response_model=ReadSchema)
async def update_fremde_eintraege(
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_einstellungs_editor),
):
    gemeinde = await db.get(Gemeinde, user.gemeinde_id)
    for key, value in updates.model_dump(exclude_unset=True, exclude_none=True).items():
        setattr(gemeinde, key, value)
    await db.commit()
    await db.refresh(gemeinde)
    return gemeinde
