from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import current_platform_admin, get_async_session
from app.crud.dokumentation_seite import crud_dokumentation_seite as crud
from app.crud.exceptions import NotFoundError
from app.models.user import User
from app.schemas.dokumentation_seite import (
    DokumentationSeiteCreate as CreateSchema,
    DokumentationSeiteRead as ReadSchema,
    DokumentationSeiteReorderUpdate,
    DokumentationSeiteUpdate as UpdateSchema,
)

router = APIRouter()


@router.get("", response_model=List[ReadSchema])
async def get_dokumentation_seiten(
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    try:
        return await crud.get_all(db, sort_params=[("reihenfolge", "asc")])
    except NotFoundError:
        return []


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ReadSchema)
async def create_dokumentation_seite(
    obj_in: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    return await crud.create(db, obj_in)


@router.patch("/{id}", response_model=ReadSchema)
async def update_dokumentation_seite(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    return await crud.update(db, id, updates)


@router.post("/reorder", response_model=List[ReadSchema])
async def reorder_dokumentation_seiten(
    obj_in: DokumentationSeiteReorderUpdate,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    return await crud.reorder(db, obj_in)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dokumentation_seite(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    await crud.delete(db, id)
