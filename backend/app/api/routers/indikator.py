from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.indikator import crud_indikator as crud
from app.core.deps import current_active_user, get_async_session
from app.models.indikator import Indikator
from app.models.user import User
from app.models.tag import Tag
from app.schemas.indikator import IndikatorCreate, IndikatorUpdate, IndikatorRead
from app.utils.auth_util import check_user_authorization
from app.utils.geteilte_eintraege import get_eigene_und_geteilte

router = APIRouter()


@router.get("", response_model=List[IndikatorRead])
async def get_indicators(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    # Eigene Einträge plus geteilte Einträge anderer Kommunen (falls aktiviert)
    return await get_eigene_und_geteilte(
        db, Indikator, user, user.gemeinde.fremde_indikatoren_anzeigen
    )


@router.get("/{id}", response_model=IndikatorRead)
async def get_indicator(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return instance


@router.post("", status_code=status.HTTP_201_CREATED, response_model=IndikatorRead)
async def create_indicator(
    indicator: IndikatorCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create_with_associations(
        db=db,
        obj_in=indicator,
        user=user,
        association_fields={"tag_ids": (Tag, "tags")},
    )


@router.patch("/{id}", response_model=IndikatorRead)
async def update_indicator(
    id: int,
    updates: IndikatorUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.update_with_associations(
        db=db,
        id=id,
        obj_in=updates,
        user=user,
        association_fields={"tag_ids": (Tag, "tags")},
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_indicator(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):

    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    await crud.delete(db, id)
