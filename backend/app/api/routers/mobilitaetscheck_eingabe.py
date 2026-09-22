from typing import List

from fastapi import APIRouter, Depends, status, Response
from sqlalchemy import or_
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.mobilitaetscheck_eingabe import crud_mobility_submission as crud
from app.core.deps import current_active_user, get_async_session, get_effective_is_politik
from app.models.user import User
from app.schemas.mobilitaetscheck_eingabe import (
    MobilitaetscheckEingabeCreate as CreateSchema,
    MobilitaetscheckEingabeUpdate as UpdateSchema,
    MobilitaetscheckEingabeRead as ReadSchema,
    MobilitaetscheckEingabeFilter as FilterSchema,
)
from app.schemas.mobilitaetscheck_eingabe_ziel_ober import (
    MobilitaetscheckEingabeZielOberCreate,
)
from app.schemas.mobilitaetscheck_eingabe_ziel_unter import (
    MobilitaetscheckEingabeZielUnterCreate,
)
from app.models.magistratsvorlage import Magistratsvorlage
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe as EingabeModel
from app.utils.auth_util import check_user_authorization
from app.api.routers.mobilitaetscheck_eingabe_ziel_ober import (
    create_mobilitaetscheck_eingabe_ziel_ober,
)
from app.api.routers.mobilitaetscheck_eingabe_ziel_unter import (
    create_mobilitaetscheck_eingabe_ziel_unter,
)
from app.crud.mobilitaetscheck_ziel_set import crud_ziel_set
from app.services.pdf.mobilitaetscheck_pdf import MobilitaetscheckPDF

router = APIRouter()


@router.get("", response_model=List[ReadSchema], status_code=status.HTTP_200_OK)
async def get_mobility_submissions(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    sort_params = [("erstellt_am", "desc")]

    return await crud.get_by_key(
        db=db,
        key="gemeinde_id",
        value=user.gemeinde_id,
        sort_params=sort_params,
    )


@router.get("/hat-eigene")
async def get_hat_eigene_mobilitaetschecks(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    """Return whether the current user has created any own Mobilitätscheck."""
    return {"hat_eigene": await crud.hat_eigene(db, user.id)}


@router.get(
    "/nach-parametern",
    response_model=List[ReadSchema],
    status_code=status.HTTP_200_OK,
)
async def filter_mobility_submissions(
    user_rolle: bool = None,
    veroeffentlicht: bool = None,
    user_id: bool = None,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    schema = FilterSchema(
        user_rolle=user_rolle,
        user_id=user_id,
        veroeffentlicht=veroeffentlicht,
    )
    # create a dictionary of keys to filter by
    keys = {
        "autor.rolle": user.rolle if schema.user_rolle else None,
        "veroeffentlicht": schema.veroeffentlicht,
        "erstellt_von": user.id if schema.user_id else None,
    }
    # Remove None values from keys
    keys = {k: v for k, v in keys.items() if v is not None}

    sort_params = [("erstellt_am", "desc")]

    return await crud.get_by_multi_keys(db=db, keys=keys, sort_params=sort_params)


@router.get(
    "/magistratsvorlage/{magistratsvorlage_id}",
    response_model=List[ReadSchema],
    status_code=status.HTTP_200_OK,
)
async def get_mobility_submission(
    magistratsvorlage_id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
    is_politik: bool = Depends(get_effective_is_politik),
):
    sort_params = [("erstellt_am", "desc")]

    if is_politik:
        stmt = (
            select(EingabeModel)
            .where(EingabeModel.magistratsvorlage_id == magistratsvorlage_id)
            .where(
                or_(
                    EingabeModel.veroeffentlicht == True,
                    EingabeModel.erstellt_von == user.id,
                )
            )
            .order_by(EingabeModel.erstellt_am.desc())
        )
        result = await db.execute(stmt)
        instances = result.scalars().all()
    else:
        try:
            instances = await crud.get_by_multi_keys(
                db=db,
                keys={"magistratsvorlage_id": magistratsvorlage_id},
                sort_params=sort_params,
            )
        except Exception:
            return Response(status_code=status.HTTP_204_NO_CONTENT)

    if not instances:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    return instances


@router.get("/{id}", response_model=ReadSchema, status_code=status.HTTP_200_OK)
async def get_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return instance


@router.post(
    "/duplizieren/{id}",
    response_model=ReadSchema,
    status_code=status.HTTP_201_CREATED,
)
async def copy_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.copy(db, id, user)


@router.get("/export/{id}", status_code=status.HTTP_201_CREATED)
async def export_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    pdf_export = await crud.export(db, id)
    # validated_instance = ReadSchema.model_validate(instance)
    # print(validated_instance.model_dump())
    # pdf = MobilitaetscheckPDF(orientation="P", unit="mm", format="A4")
    # pdf_export = pdf.export(validated_instance.model_dump())

    filename = f"mobilitaetscheck_{instance.magistratsvorlage.verwaltungsvorgang_nr}_{instance.name}.pdf"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(pdf_export, media_type="application/pdf", headers=headers)


@router.post("", response_model=ReadSchema, status_code=status.HTTP_201_CREATED)
async def create_mobilitaetscheck_eingabe(
    eingabe: CreateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.create(db=db, obj_in=eingabe, user=user)

    ziel_set = await crud_ziel_set.get(db, eingabe.ziel_set_id)
    for set_ober in sorted(ziel_set.ziele_ober, key=lambda o: o.nr):
        obj_in_ziel_ober = MobilitaetscheckEingabeZielOberCreate(
            eingabe_id=instance.id, ziel_ober_id=set_ober.id
        )
        eingabe_ziel_ober = await create_mobilitaetscheck_eingabe_ziel_ober(
            obj_in=obj_in_ziel_ober, db=db
        )
        for set_unter in sorted(set_ober.ziele_unter, key=lambda u: u.nr):
            obj_in_ziel_unter = MobilitaetscheckEingabeZielUnterCreate(
                eingabe_ziel_ober_id=eingabe_ziel_ober.id,
                ziel_unter_id=set_unter.id,
                auswirkung=0,
            )
            await create_mobilitaetscheck_eingabe_ziel_unter(
                obj_in=obj_in_ziel_unter, db=db
            )

    return instance


@router.patch("/{id}", response_model=ReadSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_mobility_submission(
    id: int,
    updates: UpdateSchema,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    instance = await crud.update(db, id, updates, user)

    if updates.veroeffentlicht is True and instance.magistratsvorlage_id is not None:
        result = await db.execute(
            select(Magistratsvorlage).where(
                Magistratsvorlage.id == instance.magistratsvorlage_id
            )
        )
        magistratsvorlage = result.scalar_one_or_none()
        if magistratsvorlage and not magistratsvorlage.veroeffentlicht:
            magistratsvorlage.veroeffentlicht = True
            await db.commit()

    return instance


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mobility_submission(
    id: int,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_user),
):
    instance = await crud.get(db, id)
    check_user_authorization(user, instance.gemeinde_id)
    return await crud.delete(db, id)
