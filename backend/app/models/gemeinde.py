from typing import Optional, List

from sqlalchemy import ARRAY, ForeignKey, String, false, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Gemeinde(Base):
    __tablename__ = "gemeinde"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
        unique=True,
        comment="Gemeinde ID",
    )
    name: Mapped[str] = mapped_column(
        nullable=False, comment="Name der Gemeinde oder Stadt"
    )
    verwaltung_email_domains: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list,
        server_default=text("'{}'"),
        comment="Erlaubte E-Mail-Domains für Verwaltung-Benutzer (z.B. muenchen.de)",
    )
    standard_ziel_set_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("mobilitaetscheck_ziel_set.id", ondelete="SET NULL"),
        nullable=True,
        comment="ID des Standard-Leitziele-Sets dieser Gemeinde",
    )
    klimacheck_aktiv: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        server_default=false(),
        comment="Klimacheck für diese Gemeinde freigeschaltet (durch Systemadmin)",
    )
    pdf_logo_dateiname: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
        comment="Dateiname des Kommunen-Logos für PDF-Exporte (in GEMEINDE_LOGO_UPLOAD_DIR)",
    )
    users: Mapped[Optional[List["User"]]] = relationship(
        back_populates="gemeinde", lazy="selectin"
    )
    gebiete: Mapped[Optional[List["GemeindeGebiet"]]] = relationship(
        back_populates="gemeinde", lazy="selectin"
    )
    einheiten: Mapped[Optional[List["GemeindeEinheit"]]] = relationship(
        back_populates="gemeinde", lazy="selectin"
    )


from app.models.user import User
from app.models.gemeinde_gebiet import GemeindeGebiet
from app.models.gemeinde_einheit import GemeindeEinheit
