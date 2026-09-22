from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import current_platform_admin, get_async_session
from app.models.gemeinde import Gemeinde
from app.models.klimarelevanzpruefung_eingabe import KlimarelevanzpruefungEingabe
from app.models.magistratsvorlage import Magistratsvorlage
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe
from app.models.user import User
from app.schemas.dashboard import DashboardStats, GemeindeZahl, MonatsZahl

router = APIRouter()


async def _count(db: AsyncSession, model) -> int:
    result = await db.execute(select(func.count()).select_from(model))
    return result.scalar_one()


async def _pro_monat(
    db: AsyncSession, model, von: Optional[date], bis: Optional[date]
) -> list[MonatsZahl]:
    monat = func.date_trunc("month", model.erstellt_am).label("monat")
    query = select(monat, func.count().label("anzahl"))
    if von is not None:
        query = query.where(model.erstellt_am >= von)
    if bis is not None:
        query = query.where(model.erstellt_am < bis)
    query = query.group_by(monat).order_by(monat)
    result = await db.execute(query)
    return [MonatsZahl(monat=row.monat.date(), anzahl=row.anzahl) for row in result.all()]


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    von: Optional[date] = None,
    bis: Optional[date] = None,
    db: AsyncSession = Depends(get_async_session),
    _: User = Depends(current_platform_admin),
):
    anzahl_user = await _count(db, User)
    anzahl_gemeinden = await _count(db, Gemeinde)
    anzahl_magistratsvorlagen = await _count(db, Magistratsvorlage)
    anzahl_mobilitaetschecks = await _count(db, MobilitaetscheckEingabe)
    anzahl_klimarelevanzpruefungen = await _count(db, KlimarelevanzpruefungEingabe)

    result = await db.execute(
        select(func.count()).select_from(Magistratsvorlage).where(Magistratsvorlage.veroeffentlicht.is_(True))
    )
    magistratsvorlagen_veroeffentlicht = result.scalar_one()

    neue_user_pro_monat = await _pro_monat(db, User, von, bis)
    neue_magistratsvorlagen_pro_monat = await _pro_monat(db, Magistratsvorlage, von, bis)
    neue_mobilitaetschecks_pro_monat = await _pro_monat(db, MobilitaetscheckEingabe, von, bis)
    neue_klimarelevanzpruefungen_pro_monat = await _pro_monat(
        db, KlimarelevanzpruefungEingabe, von, bis
    )

    result = await db.execute(
        select(Gemeinde.name, func.count(Magistratsvorlage.id).label("anzahl"))
        .join(Magistratsvorlage, Magistratsvorlage.gemeinde_id == Gemeinde.id)
        .group_by(Gemeinde.name)
        .order_by(func.count(Magistratsvorlage.id).desc())
    )
    magistratsvorlagen_pro_gemeinde = [
        GemeindeZahl(gemeinde=row.name, anzahl=row.anzahl) for row in result.all()
    ]

    return DashboardStats(
        anzahl_user=anzahl_user,
        anzahl_gemeinden=anzahl_gemeinden,
        anzahl_magistratsvorlagen=anzahl_magistratsvorlagen,
        anzahl_mobilitaetschecks=anzahl_mobilitaetschecks,
        anzahl_klimarelevanzpruefungen=anzahl_klimarelevanzpruefungen,
        magistratsvorlagen_veroeffentlicht=magistratsvorlagen_veroeffentlicht,
        neue_user_pro_monat=neue_user_pro_monat,
        neue_magistratsvorlagen_pro_monat=neue_magistratsvorlagen_pro_monat,
        neue_mobilitaetschecks_pro_monat=neue_mobilitaetschecks_pro_monat,
        neue_klimarelevanzpruefungen_pro_monat=neue_klimarelevanzpruefungen_pro_monat,
        magistratsvorlagen_pro_gemeinde=magistratsvorlagen_pro_gemeinde,
    )
