from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

if TYPE_CHECKING:
    from app.models.branding_asset import BrandingAsset


class LogoListeEintrag(Base):
    __tablename__ = "logo_liste_eintrag"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, nullable=False, unique=True, comment="Logo-Listeneintrag ID"
    )
    bereich: Mapped[str] = mapped_column(
        nullable=False,
        index=True,
        comment="Seitenbereich der Logo-Liste (z.B. 'footer', 'login')",
    )
    asset_id: Mapped[int] = mapped_column(
        ForeignKey("branding_asset.id", ondelete="CASCADE"),
        nullable=False,
        comment="Zugewiesenes Branding-Asset",
    )
    link: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Optionales Link-Ziel, das beim Klick auf das Logo geöffnet wird"
    )
    reihenfolge: Mapped[int] = mapped_column(
        nullable=False, default=0, comment="Anzeigereihenfolge innerhalb des Bereichs (aufsteigend)"
    )

    asset: Mapped["BrandingAsset"] = relationship(lazy="selectin")
