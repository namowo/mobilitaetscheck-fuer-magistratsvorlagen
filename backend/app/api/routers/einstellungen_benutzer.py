from typing import Optional
from uuid import UUID as UUIDType

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.deps import current_gemeinde_admin, get_async_session
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter()


class GemeindeUserUpdate(BaseModel):
    rolle_id: Optional[int] = None
    is_local_superuser: Optional[bool] = None
    gruppe_id: Optional[int] = None


@router.patch("/{user_id}", response_model=UserRead)
async def update_gemeinde_user(
    user_id: UUIDType,
    obj_in: GemeindeUserUpdate,
    db: AsyncSession = Depends(get_async_session),
    admin: User = Depends(current_gemeinde_admin),
):
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.gemeinde_id == admin.gemeinde_id,
        )
    )
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Benutzer nicht gefunden")
    if obj_in.rolle_id is not None:
        target.rolle_id = obj_in.rolle_id
    if obj_in.is_local_superuser is not None:
        target.is_local_superuser = obj_in.is_local_superuser
    if "gruppe_id" in obj_in.model_fields_set:
        target.gruppe_id = obj_in.gruppe_id
    await db.commit()
    await db.refresh(target)
    return target


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_gemeinde_user(
    user_id: UUIDType,
    db: AsyncSession = Depends(get_async_session),
    admin: User = Depends(current_gemeinde_admin),
):
    result = await db.execute(
        select(User).where(
            User.id == user_id,
            User.gemeinde_id == admin.gemeinde_id,
        )
    )
    target = result.scalar_one_or_none()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Benutzer nicht gefunden")
    await db.delete(target)
    await db.commit()
