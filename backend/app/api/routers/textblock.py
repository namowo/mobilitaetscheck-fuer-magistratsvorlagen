from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.textblock import crud_textblock as crud
from app.core.deps import current_active_user, get_async_session
from app.models.textblock import Textblock
from app.models.user import User
from app.models.tag import Tag
from app.schemas.textblock import (
    TextblockCreate as CreateSchema,
    TextblockUpdate as UpdateSchema,
    TextblockRead as ReadSchema,
)
from app.utils.auth_util import check_user_authorization
from app.utils.geteilte_eintraege import get_eigene_und_geteilte

router = APIRouter()

association_fields = {"tag_ids": (Tag, "tags")}


@router.get("", response_model=List[ReadSchema])
async def get_all_text_blocks(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    # Eigene Einträge plus geteilte Einträge anderer Kommunen (falls aktiviert)
    return await get_eigene_und_geteilte(
        db, Textblock, user, user.gemeinde.fremde_textbausteine_anzeigen
    )


@router.get("/{id}", response_model=ReadSchema)
async def get_text_block(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return instance


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReadSchema)
async def create_text_block(
    obj_in: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    return await crud.create_with_associations(
        db=db,
        obj_in=obj_in,
        user=user,
        association_fields=association_fields,
    )


@router.patch("/{id}", response_model=ReadSchema)
async def update_text_block(
    id: int,
    updates: UpdateSchema,
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
        association_fields=association_fields,
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_text_block(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    await crud.delete(db, id)
