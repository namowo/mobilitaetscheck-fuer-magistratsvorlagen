from typing import Optional

from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import text, false

from app.core.db import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    is_local_superuser: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=false(),
        comment="Gemeinde-Admin: Adminrechte innerhalb der eigenen Gemeinde (unabhängig von is_superuser, das nur Plattform-Administratoren vorbehalten ist)",
    )
    vorname: Mapped[str] = mapped_column(
        nullable=False, comment="Vorname des Benutzers"
    )
    nachname: Mapped[str] = mapped_column(
        nullable=False, comment="Nachname des Benutzers"
    )
    rolle_id: Mapped[int] = mapped_column(
        ForeignKey("user_rolle.id", ondelete="SET NULL"),
        nullable=False,
        comment="Rolle ID des Benutzers",
    )
    rolle: Mapped["UserRolle"] = relationship(back_populates="users", lazy="selectin")
    gemeinde_id: Mapped[int] = mapped_column(
        ForeignKey("gemeinde.id", ondelete="CASCADE"),
        nullable=False,
        comment="Gemeinde ID, mit der der Benutzer verknüpft ist",
    )
    gemeinde: Mapped["Gemeinde"] = relationship(back_populates="users", lazy="selectin")
    einheit_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("gemeinde_einheit.id", ondelete="SET NULL"),
        nullable=True,
        comment="Einheit des Benutzers innerhalb der Gemeinde",
    )
    einheit: Mapped[Optional["GemeindeEinheit"]] = relationship(lazy="selectin")
    gruppe_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("user_gruppe.id", ondelete="SET NULL"),
        nullable=True,
        comment="Gruppe des Benutzers",
    )
    gruppe: Mapped[Optional["UserGruppe"]] = relationship(lazy="selectin")
    erstellt_am: Mapped[datetime] = mapped_column(
        nullable=False,
        server_default=text("now()"),
        comment="Zeitpunkt der Erstellung des Benutzers",
    )


from app.models.gemeinde import Gemeinde
from app.models.gemeinde_einheit import GemeindeEinheit
from app.models.user_rolle import UserRolle
from app.models.user_gruppe import UserGruppe
