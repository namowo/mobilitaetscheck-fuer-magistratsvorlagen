from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.deps import current_active_user, get_async_session
from app.crud.exceptions import DatabaseCommitError, NotFoundError
from app.crud.mobilitaetscheck_ziel_set import crud_ziel_set
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe
from app.models.mobilitaetscheck_eingabe_ziel_ober import MobilitaetscheckEingabeZielOber
from app.models.mobilitaetscheck_ziel_set_ober import MobilitaetscheckZielSetOber as Model
from app.models.user import User
from app.schemas.mobilitaetscheck_ziel_set import MobilitaetscheckZielSetOberRead as ReadSchema
from app.utils.auth_util import check_user_authorization

router = APIRouter()


class ZielSetOberCreate(BaseModel):
    ziel_set_id: int
    name: str


class ZielSetOberUpdate(BaseModel):
    name: str


class ZielSetOberReorderRequest(BaseModel):
    ziel_set_id: int
    ids: List[int]


async def _get_ober(db: AsyncSession, id: int) -> Model:
    result = await db.execute(select(Model).where(Model.id == id))
    instance = result.scalars().first()
    if instance is None:
        raise NotFoundError("MobilitaetscheckZielSetOber")
    return instance


@router.post("", response_model=ReadSchema, status_code=status.HTTP_201_CREATED)
async def create_ziel_set_ober(
    obj_in: ZielSetOberCreate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    ziel_set = await crud_ziel_set.get(db, obj_in.ziel_set_id)
    check_user_authorization(user, ziel_set.gemeinde_id)

    max_nr = max((o.nr for o in ziel_set.ziele_ober), default=0)
    new_ober = Model(nr=max_nr + 1, name=obj_in.name, ziel_set_id=obj_in.ziel_set_id)
    db.add(new_ober)
    try:
        await db.commit()
        await db.refresh(new_ober)
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)

    # Propagate: create EingabeZielOber for all existing Eingaben that use this ZielSet
    eingaben_result = await db.execute(
        select(MobilitaetscheckEingabe).where(MobilitaetscheckEingabe.ziel_set_id == obj_in.ziel_set_id)
    )
    for eingabe in eingaben_result.scalars().all():
        db.add(MobilitaetscheckEingabeZielOber(eingabe_id=eingabe.id, ziel_ober_id=new_ober.id, tangiert=False))
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)

    return new_ober


@router.patch("/{id}", response_model=ReadSchema)
async def update_ziel_set_ober(
    id: int,
    updates: ZielSetOberUpdate,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    ober = await _get_ober(db, id)
    ziel_set = await crud_ziel_set.get(db, ober.ziel_set_id)
    check_user_authorization(user, ziel_set.gemeinde_id)
    ober.name = updates.name
    try:
        await db.commit()
        await db.refresh(ober)
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)
    return ober


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ziel_set_ober(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    ober = await _get_ober(db, id)
    ziel_set = await crud_ziel_set.get(db, ober.ziel_set_id)
    check_user_authorization(user, ziel_set.gemeinde_id)
    ziel_set_id = ober.ziel_set_id
    await db.delete(ober)
    await db.flush()
    siblings = await db.execute(select(Model).where(Model.ziel_set_id == ziel_set_id).order_by(Model.nr))
    for i, sibling in enumerate(siblings.scalars().all()):
        sibling.nr = i + 1
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)


@router.post("/reorder", status_code=status.HTTP_204_NO_CONTENT)
async def reorder_ziel_set_ober(
    body: ZielSetOberReorderRequest,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    ziel_set = await crud_ziel_set.get(db, body.ziel_set_id)
    check_user_authorization(user, ziel_set.gemeinde_id)

    for i, ober_id in enumerate(body.ids):
        ober = await _get_ober(db, ober_id)
        ober.nr = i + 1
    try:
        await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()
        raise DatabaseCommitError(e)
