from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.crud.base import CRUDBase
from app.models.dokumentation_seite import DokumentationSeite as Model
from app.schemas.dokumentation_seite import (
    DokumentationSeiteCreate as CreateSchema,
    DokumentationSeiteReorderUpdate,
    DokumentationSeiteUpdate as UpdateSchema,
)


class CRUDDokumentationSeite(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)

    async def create(self, db: AsyncSession, obj_in: CreateSchema, user=None) -> Model:
        max_result = await db.execute(select(func.max(Model.reihenfolge)))
        max_reihenfolge = max_result.scalar_one_or_none()
        next_reihenfolge = (max_reihenfolge + 1) if max_reihenfolge is not None else 0

        instance = Model(
            titel=obj_in.titel,
            slug=obj_in.slug,
            inhalt=obj_in.inhalt,
            zeigt_kontakt_button=obj_in.zeigt_kontakt_button,
            reihenfolge=next_reihenfolge,
        )
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    async def reorder(
        self, db: AsyncSession, obj_in: DokumentationSeiteReorderUpdate
    ) -> list[Model]:
        ids = [item.id for item in obj_in.reihenfolge]
        result = await db.execute(select(Model).where(Model.id.in_(ids)))
        instances_by_id = {i.id: i for i in result.scalars().all()}
        for item in obj_in.reihenfolge:
            instance = instances_by_id.get(item.id)
            if instance is not None:
                instance.reihenfolge = item.reihenfolge
        await db.commit()
        return await self.get_all(db, sort_params=[("reihenfolge", "asc")])


crud_dokumentation_seite = CRUDDokumentationSeite()
