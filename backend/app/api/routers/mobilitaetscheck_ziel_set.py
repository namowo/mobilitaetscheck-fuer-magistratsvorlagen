from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.mobilitaetscheck_ziel_set import crud_ziel_set as crud
from app.core.deps import current_active_user, get_async_session
from app.models.user import User
from app.models.gemeinde import Gemeinde
from app.schemas.mobilitaetscheck_ziel_set import (
    MobilitaetscheckZielSetCreate as CreateSchema,
    MobilitaetscheckZielSetUpdate as UpdateSchema,
    MobilitaetscheckZielSetRead as ReadSchema,
    MobilitaetscheckZielSetListRead as ListReadSchema,
    MobilitaetscheckZielSetKopierenRequest,
)
from app.utils.auth_util import check_user_authorization
from app.crud.exceptions import DatabaseCommitError

router = APIRouter()


async def _get_gemeinde(db: AsyncSession, gemeinde_id: int) -> Gemeinde:
    result = await db.execute(select(Gemeinde).where(Gemeinde.id == gemeinde_id))
    return result.scalars().first()


@router.get("", response_model=List[ListReadSchema])
async def get_ziel_sets(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Return own sets and all public sets, with ist_standard flag for the user's municipality."""
    sets = await crud.get_accessible(db, user.gemeinde_id)
    gemeinde = await _get_gemeinde(db, user.gemeinde_id)
    standard_id = gemeinde.standard_ziel_set_id if gemeinde else None

    result = []
    for s in sets:
        item = ListReadSchema.model_validate(s)
        if standard_id is not None and s.id == standard_id:
            item = item.model_copy(update={"ist_standard": True})
        result.append(item)
    return result


@router.get("/hat-eigene")
async def get_hat_eigene_ziel_sets(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Return whether the user's Gemeinde has created any own Leitziele-Set."""
    return {"hat_eigene": await crud.hat_eigene(db, user.gemeinde_id)}


@router.get("/{id}", response_model=ReadSchema)
async def get_ziel_set(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    # Allow access if own set or public
    if instance.gemeinde_id != user.gemeinde_id and not instance.ist_oeffentlich and not user.is_superuser and not user.is_local_superuser:
        from app.crud.exceptions import AuthorizationError
        raise AuthorizationError("Kein Zugriff auf dieses Set")
    return instance


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReadSchema)
async def create_ziel_set(
    obj_in: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create_with_ziele(db, obj_in, user)


@router.post("/aus-leitzielen", status_code=status.HTTP_201_CREATED, response_model=ReadSchema)
async def create_ziel_set_aus_leitzielen(
    name: str,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
    beschreibung: str = None,
    ist_oeffentlich: bool = False,
):
    """Create a ZielSet snapshot from the user's current active Leitziele."""
    return await crud.create_from_aktuelle_leitziele(db, name, beschreibung, ist_oeffentlich, user)


@router.patch("/{id}", response_model=ReadSchema)
async def update_ziel_set(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.update(db, id, updates, user)


@router.delete("/standard", status_code=status.HTTP_204_NO_CONTENT)
async def clear_standard(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Remove the standard ZielSet setting for the current municipality."""
    gemeinde = await _get_gemeinde(db, user.gemeinde_id)
    gemeinde.standard_ziel_set_id = None
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ziel_set(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    await crud.delete(db, id)


@router.post("/{id}/kopieren", status_code=status.HTTP_204_NO_CONTENT)
async def kopieren_zu_leitziele(
    id: int,
    request: MobilitaetscheckZielSetKopierenRequest,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Copy the ZielSet's Ziele into the user's own active Leitziele."""
    instance = await crud.get(db, id)
    # Allow access if own set or public
    if instance.gemeinde_id != user.gemeinde_id and not instance.ist_oeffentlich and not user.is_superuser and not user.is_local_superuser:
        from app.crud.exceptions import AuthorizationError
        raise AuthorizationError("Kein Zugriff auf dieses Set")
    await crud.kopieren_zu_leitziele(db, id, user, request.modus)


@router.post("/{id}/duplizieren", response_model=ReadSchema, status_code=status.HTTP_201_CREATED)
async def duplizieren(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Create a deep copy of a ZielSet (own or public) within the user's municipality."""
    instance = await crud.get(db, id)
    if instance.gemeinde_id != user.gemeinde_id and not instance.ist_oeffentlich and not user.is_superuser and not user.is_local_superuser:
        from app.crud.exceptions import AuthorizationError
        raise AuthorizationError("Kein Zugriff auf dieses Set")
    return await crud.duplizieren(db, id, user)


@router.post("/{id}/als-standard-setzen", status_code=status.HTTP_204_NO_CONTENT)
async def set_als_standard(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Set a ZielSet as the standard for the current municipality."""
    instance = await crud.get(db, id)
    # Allow access if own set or public
    if instance.gemeinde_id != user.gemeinde_id and not instance.ist_oeffentlich and not user.is_superuser and not user.is_local_superuser:
        from app.crud.exceptions import AuthorizationError
        raise AuthorizationError("Kein Zugriff auf dieses Set")

    gemeinde = await _get_gemeinde(db, user.gemeinde_id)
    gemeinde.standard_ziel_set_id = id
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)
