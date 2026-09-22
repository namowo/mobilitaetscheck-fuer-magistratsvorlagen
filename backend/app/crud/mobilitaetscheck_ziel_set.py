from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from app.crud.base import CRUDBase
from app.crud.exceptions import DatabaseCommitError, NotFoundError
from app.models.mobilitaetscheck_ziel_set import MobilitaetscheckZielSet as Model
from app.models.mobilitaetscheck_ziel_set_ober import MobilitaetscheckZielSetOber
from app.models.mobilitaetscheck_ziel_set_unter import MobilitaetscheckZielSetUnter
from app.models.mobilitaetscheck_ziel_ober import MobilitaetscheckZielOber
from app.models.mobilitaetscheck_ziel_unter import MobilitaetscheckZielUnter
from app.models.user import User
from app.schemas.mobilitaetscheck_ziel_set import (
    MobilitaetscheckZielSetCreate as CreateSchema,
    MobilitaetscheckZielSetUpdate as UpdateSchema,
)


class CRUDZielSet(CRUDBase[Model, CreateSchema, UpdateSchema]):
    def __init__(self):
        super().__init__(Model)

    async def get_accessible(self, db: AsyncSession, gemeinde_id: int) -> List[Model]:
        """Return own sets plus public sets from other Kommunen."""
        statement = select(self.model).where(
            or_(
                self.model.gemeinde_id == gemeinde_id,
                self.model.ist_oeffentlich == True,
            )
        ).order_by(self.model.name)
        result = await db.execute(statement)
        return result.scalars().all()

    async def get_own(self, db: AsyncSession, gemeinde_id: int) -> List[Model]:
        """Return only sets owned by this municipality."""
        statement = select(self.model).where(
            self.model.gemeinde_id == gemeinde_id
        ).order_by(self.model.name)
        result = await db.execute(statement)
        return result.scalars().all()

    async def hat_eigene(self, db: AsyncSession, gemeinde_id: int) -> bool:
        """Return whether this municipality owns at least one ZielSet."""
        statement = select(self.model.id).where(
            self.model.gemeinde_id == gemeinde_id
        ).limit(1)
        result = await db.execute(statement)
        return result.scalar_one_or_none() is not None

    async def create_with_ziele(
        self, db: AsyncSession, obj_in: CreateSchema, user: User
    ) -> Model:
        """Create a new ZielSet with nested ZielSetOber and ZielSetUnter."""
        new_set = Model(
            name=obj_in.name,
            beschreibung=obj_in.beschreibung,
            ist_oeffentlich=obj_in.ist_oeffentlich,
            gemeinde_id=user.gemeinde_id,
            erstellt_von=user.id,
            zuletzt_bearbeitet_von=user.id,
        )
        db.add(new_set)

        for ober_in in obj_in.ziele_ober:
            new_ober = MobilitaetscheckZielSetOber(
                nr=ober_in.nr,
                name=ober_in.name,
                ziel_set=new_set,
            )
            db.add(new_ober)
            for unter_in in ober_in.ziele_unter:
                new_unter = MobilitaetscheckZielSetUnter(
                    nr=unter_in.nr,
                    name=unter_in.name,
                    ziel_set_ober=new_ober,
                )
                db.add(new_unter)

        try:
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseCommitError(e)

        return await self.get(db, new_set.id)

    async def create_from_aktuelle_leitziele(
        self, db: AsyncSession, name: str, beschreibung: Optional[str], ist_oeffentlich: bool, user: User
    ) -> Model:
        """Create a ZielSet snapshot from the currently active Leitziele of the user's municipality."""
        # Fetch active Oberziele
        stmt_ober = (
            select(MobilitaetscheckZielOber)
            .where(MobilitaetscheckZielOber.gemeinde_id == user.gemeinde_id)
            .order_by(MobilitaetscheckZielOber.nr)
        )
        result_ober = await db.execute(stmt_ober)
        aktuelle_ober = result_ober.scalars().all()

        new_set = Model(
            name=name,
            beschreibung=beschreibung,
            ist_oeffentlich=ist_oeffentlich,
            gemeinde_id=user.gemeinde_id,
            erstellt_von=user.id,
            zuletzt_bearbeitet_von=user.id,
        )
        db.add(new_set)

        for ober in aktuelle_ober:
            new_ober = MobilitaetscheckZielSetOber(
                nr=ober.nr,
                name=ober.name,
                ziel_set=new_set,
            )
            db.add(new_ober)

            stmt_unter = (
                select(MobilitaetscheckZielUnter)
                .where(MobilitaetscheckZielUnter.ziel_ober_id == ober.id)
                .order_by(MobilitaetscheckZielUnter.nr)
            )
            result_unter = await db.execute(stmt_unter)
            aktuelle_unter = result_unter.scalars().all()

            for unter in aktuelle_unter:
                new_unter = MobilitaetscheckZielSetUnter(
                    nr=unter.nr,
                    name=unter.name,
                    ziel_set_ober=new_ober,
                )
                db.add(new_unter)

        try:
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseCommitError(e)

        return await self.get(db, new_set.id)

    async def duplizieren(self, db: AsyncSession, set_id: int, user: User) -> Model:
        """Create a deep copy of a ZielSet within the user's municipality."""
        original = await self.get(db, set_id)

        if original.gemeinde_id != user.gemeinde_id:
            copy_name = f"Kopie von {original.gemeinde.name}"
        else:
            copy_name = f"Kopie von {original.name}"

        new_set = Model(
            name=copy_name,
            beschreibung=original.beschreibung,
            ist_oeffentlich=False,
            gemeinde_id=user.gemeinde_id,
            erstellt_von=user.id,
            zuletzt_bearbeitet_von=user.id,
        )
        db.add(new_set)

        for ober in sorted(original.ziele_ober, key=lambda o: o.nr):
            new_ober = MobilitaetscheckZielSetOber(nr=ober.nr, name=ober.name, ziel_set=new_set)
            db.add(new_ober)
            for unter in sorted(ober.ziele_unter, key=lambda u: u.nr):
                db.add(MobilitaetscheckZielSetUnter(nr=unter.nr, name=unter.name, ziel_set_ober=new_ober))

        try:
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseCommitError(e)

        return await self.get(db, new_set.id)

    async def kopieren_zu_leitziele(
        self, db: AsyncSession, set_id: int, user: User, modus: str
    ) -> None:
        """Copy a ZielSet's Ziele into the user's active Leitziele.

        modus: 'ersetzen' deletes all existing Leitziele first,
               'anhaengen' appends after existing ones.
        """
        ziel_set = await self.get(db, set_id)

        if modus == "ersetzen":
            # Delete all existing Oberziele (Unterziele cascade)
            stmt = select(MobilitaetscheckZielOber).where(
                MobilitaetscheckZielOber.gemeinde_id == user.gemeinde_id
            )
            result = await db.execute(stmt)
            existing = result.scalars().all()
            for item in existing:
                await db.delete(item)
            await db.flush()
            start_nr = 1
        else:
            # Append: find the highest existing nr
            stmt = select(MobilitaetscheckZielOber).where(
                MobilitaetscheckZielOber.gemeinde_id == user.gemeinde_id
            )
            result = await db.execute(stmt)
            existing = result.scalars().all()
            start_nr = max((o.nr for o in existing), default=0) + 1

        # Sort set Oberziele by nr
        sorted_ober = sorted(ziel_set.ziele_ober, key=lambda o: o.nr)

        for i, set_ober in enumerate(sorted_ober):
            new_ober = MobilitaetscheckZielOber(
                nr=start_nr + i,
                name=set_ober.name,
                gemeinde_id=user.gemeinde_id,
                erstellt_von=user.id,
                zuletzt_bearbeitet_von=user.id,
            )
            db.add(new_ober)
            await db.flush()

            sorted_unter = sorted(set_ober.ziele_unter, key=lambda u: u.nr)
            for j, set_unter in enumerate(sorted_unter):
                new_unter = MobilitaetscheckZielUnter(
                    nr=j + 1,
                    name=set_unter.name,
                    ziel_ober_id=new_ober.id,
                    gemeinde_id=user.gemeinde_id,
                    erstellt_von=user.id,
                    zuletzt_bearbeitet_von=user.id,
                )
                db.add(new_unter)

        try:
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise DatabaseCommitError(e)


crud_ziel_set = CRUDZielSet()
