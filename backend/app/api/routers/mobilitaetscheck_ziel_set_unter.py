from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.deps import current_active_user, get_async_session
from app.crud.exceptions import DatabaseCommitError, NotFoundError
from app.crud.mobilitaetscheck_ziel_set import crud_ziel_set
from app.models.mobilitaetscheck_eingabe_ziel_ober import MobilitaetscheckEingabeZielOber
from app.models.mobilitaetscheck_eingabe_ziel_unter import MobilitaetscheckEingabeZielUnter
from app.models.mobilitaetscheck_ziel_set_ober import MobilitaetscheckZielSetOber
from app.models.mobilitaetscheck_ziel_set_unter import MobilitaetscheckZielSetUnter as Model
from app.models.user import User
from app.schemas.mobilitaetscheck_ziel_set import MobilitaetscheckZielSetUnterRead as ReadSchema
from app.utils.auth_util import check_user_authorization

router = APIRouter()


class ZielSetUnterCreate(BaseModel):
    ziel_set_ober_id: int
    name: str


class ZielSetUnterUpdate(BaseModel):
    name: str


class ZielSetUnterReorderRequest(BaseModel):
    ziel_set_ober_id: int
    ids: List[int]


async def _get_unter(db: AsyncSession, id: int) -> Model:
    result = await db.execute(select(Model).where(Model.id == id))
    instance = result.scalars().first()
    if instance is None:
        raise NotFoundError("MobilitaetscheckZielSetUnter")
    return instance


async def _get_ober(db: AsyncSession, id: int) -> MobilitaetscheckZielSetOber:
    result = await db.execute(select(MobilitaetscheckZielSetOber).where(MobilitaetscheckZielSetOber.id == id))
    instance = result.scalars().first()
    if instance is None:
        raise NotFoundError("MobilitaetscheckZielSetOber")
    return instance


@router.post("", response_model=ReadSchema, status_code=status.HTTP_201_CREATED)
async def create_ziel_set_unter(
    obj_in: ZielSetUnterCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    ober = await _get_ober(db, obj_in.ziel_set_ober_id)
    ziel_set = await crud_ziel_set.get(db, ober.ziel_set_id)
    check_user_authorization(user, ziel_set.gemeinde_id)

    max_nr = max((u.nr for u in ober.ziele_unter), default=0)
    new_unter = Model(nr=max_nr + 1, name=obj_in.name, ziel_set_ober_id=obj_in.ziel_set_ober_id)
    db.add(new_unter)
    try:
        await db.commit()
        await db.refresh(new_unter)
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)

    # Propagate: create EingabeZielUnter for all existing EingabeZielOber that reference this ZielSetOber
    eingabe_ober_result = await db.execute(
        select(MobilitaetscheckEingabeZielOber).where(
            MobilitaetscheckEingabeZielOber.ziel_ober_id == obj_in.ziel_set_ober_id
        )
    )
    for eingabe_ober in eingabe_ober_result.scalars().all():
        db.add(MobilitaetscheckEingabeZielUnter(
            eingabe_ziel_ober_id=eingabe_ober.id,
            ziel_unter_id=new_unter.id,
            tangiert=False,
        ))
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)

    return new_unter


@router.patch("/{id}", response_model=ReadSchema)
async def update_ziel_set_unter(
    id: int,
    updates: ZielSetUnterUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    unter = await _get_unter(db, id)
    ober = await _get_ober(db, unter.ziel_set_ober_id)
    ziel_set = await crud_ziel_set.get(db, ober.ziel_set_id)
    check_user_authorization(user, ziel_set.gemeinde_id)
    unter.name = updates.name
    try:
        await db.commit()
        await db.refresh(unter)
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)
    return unter


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ziel_set_unter(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    unter = await _get_unter(db, id)
    ober = await _get_ober(db, unter.ziel_set_ober_id)
    ziel_set = await crud_ziel_set.get(db, ober.ziel_set_id)
    check_user_authorization(user, ziel_set.gemeinde_id)
    ober_id = unter.ziel_set_ober_id
    await db.delete(unter)
    await db.flush()
    siblings = await db.execute(select(Model).where(Model.ziel_set_ober_id == ober_id).order_by(Model.nr))
    for i, sibling in enumerate(siblings.scalars().all()):
        sibling.nr = i + 1
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)


@router.post("/reorder", status_code=status.HTTP_204_NO_CONTENT)
async def reorder_ziel_set_unter(
    body: ZielSetUnterReorderRequest,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    ober = await _get_ober(db, body.ziel_set_ober_id)
    ziel_set = await crud_ziel_set.get(db, ober.ziel_set_id)
    check_user_authorization(user, ziel_set.gemeinde_id)

    for i, unter_id in enumerate(body.ids):
        unter = await _get_unter(db, unter_id)
        unter.nr = i + 1
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)
