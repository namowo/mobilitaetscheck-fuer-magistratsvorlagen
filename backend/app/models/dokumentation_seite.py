from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class DokumentationSeite(Base):
    __tablename__ = "dokumentation_seite"

    id: Mapped[int] = mapped_column(
        primary_key=True, index=True, nullable=False, unique=True, comment="Dokumentationsseite ID"
    )
    titel: Mapped[str] = mapped_column(nullable=False, comment="Titel der Dokumentationsseite")
    slug: Mapped[str] = mapped_column(
        nullable=False, unique=True, index=True, comment="Eindeutiger Anker-Slug der Seite"
    )
    inhalt: Mapped[Optional[str]] = mapped_column(
        nullable=True, comment="Rich-Text-Inhalt der Dokumentationsseite (HTML)"
    )
    reihenfolge: Mapped[int] = mapped_column(
        nullable=False, default=0, comment="Anzeigereihenfolge der Seite (aufsteigend)"
    )
    zeigt_kontakt_button: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
        comment="Zeigt einen 'Kontakt aufnehmen'-Button unterhalb des Seiteninhalts an",
    )
