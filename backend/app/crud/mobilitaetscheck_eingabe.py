from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base_eingabe import CRUDEingabe
from app.models.mobilitaetscheck_eingabe import MobilitaetscheckEingabe as Model
from app.models.user import User
from app.schemas.mobilitaetscheck_eingabe import (
    MobilitaetscheckEingabeCreate as CreateSchema,
    MobilitaetscheckEingabeUpdate as UpdateSchema,
)
from app.services.pdf.mobilitaetscheck_pdf import MobilitaetscheckPDF


class CRUDMobilitySubmission(CRUDEingabe[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)

    async def copy(self, db: AsyncSession, id: int, user: User) -> Model:
        original = await self.get(db, id)
        exclude = ["id", "erstellt_am"]

        updates = {
            "erstellt_von": user.id,
            "zuletzt_bearbeitet_von": user.id,
            "veroeffentlicht": False,
            "name": f"Kopie von {original.name}",
        }

        nested_attributes = {
            "eingabe_ziel_ober": ["eingabe_ziel_unter"],
        }

        return await super().copy(
            db=db,
            id=id,
            updates=updates,
            exclude=exclude,
            nested_attributes=nested_attributes,
        )

    async def export(self, db: AsyncSession, id: int):
        return await super().export(db=db, id=id, PDF=MobilitaetscheckPDF)

    async def hat_eigene(self, db: AsyncSession, user_id: UUID) -> bool:
        """Return whether this user has created any Mobilitätscheck."""
        statement = select(self.model.id).where(self.model.erstellt_von == user_id).limit(1)
        result = await db.execute(statement)
        return result.scalar_one_or_none() is not None


crud_mobility_submission = CRUDMobilitySubmission()
