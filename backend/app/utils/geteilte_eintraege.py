from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gemeinde import Gemeinde
from app.models.user import User


async def get_eigene_und_geteilte(
    db: AsyncSession, model, user: User, fremde_anzeigen: bool
):
    """
    Eigene Einträge der Kommune plus – falls die Kommune das aktiviert hat – die für andere
    sichtbaren Einträge anderer Kommunen, sofern deren Kommune das Teilen erlaubt.
    Gilt für Tags, Indikatoren und Textbausteine.
    """
    bedingung = model.gemeinde_id == user.gemeinde_id
    if fremde_anzeigen:
        teilende_gemeinden = select(Gemeinde.id).where(Gemeinde.inhalte_teilen.is_(True))
        bedingung = or_(
            bedingung,
            and_(
                model.gemeindespezifisch.is_(False),
                model.gemeinde_id.in_(teilende_gemeinden),
            ),
        )
    result = await db.execute(select(model).where(bedingung).order_by(model.name.asc()))
    return result.scalars().all()
