import re
from typing import Any, Literal, Optional
from app.core.config import DEFAULT_PDF_FOOTER_TEXT
from pydantic import BaseModel, Field, ConfigDict, field_validator

RechtstextModus = Literal["inhalt", "url"]
HEX_COLOR_PATTERN = r"^#[0-9A-Fa-f]{6}$"
STARTSEITE_BLOCK_TYPEN = {
    "hero",
    "text",
    "video",
    "kacheln",
    "kennzahlen",
    "schritte",
    "faq",
    "aufruf",
}
STARTSEITE_MAX_BLOECKE = 50


class PlattformEinstellungBase(BaseModel):
    datenschutzerklaerung: Optional[str] = Field(
        None, description="Datenschutzerklärung (HTML), die bei der Registrierung angezeigt wird."
    )
    datenschutz_modus: RechtstextModus = Field(
        "inhalt", description="Wie die Datenschutzerklärung bereitgestellt wird."
    )
    datenschutz_url: Optional[str] = Field(
        None, description="Externe URL der Datenschutzerklärung, falls datenschutz_modus='url'."
    )
    impressum_modus: RechtstextModus = Field(
        "inhalt", description="Wie das Impressum bereitgestellt wird."
    )
    impressum_inhalt: Optional[str] = Field(
        None, description="Impressum (HTML), falls impressum_modus='inhalt'."
    )
    impressum_url: Optional[str] = Field(
        None, description="Externe URL des Impressums, falls impressum_modus='url'."
    )
    nutzungsbedingungen_modus: RechtstextModus = Field(
        "inhalt", description="Wie die Nutzungsbedingungen bereitgestellt werden."
    )
    nutzungsbedingungen_inhalt: Optional[str] = Field(
        None, description="Nutzungsbedingungen (HTML), falls nutzungsbedingungen_modus='inhalt'."
    )
    nutzungsbedingungen_url: Optional[str] = Field(
        None, description="Externe URL der Nutzungsbedingungen, falls nutzungsbedingungen_modus='url'."
    )
    ueber_das_tool_inhalt: Optional[str] = Field(
        None, description="Inhalt (HTML) der Seite 'Über das Tool'."
    )
    startseite_titel: Optional[str] = Field(None, description="Titel des Hero-Bereichs der Startseite.")
    startseite_untertitel: Optional[str] = Field(
        None, description="Untertitel des Hero-Bereichs der Startseite."
    )
    startseite_inhalt: Optional[str] = Field(
        None, description="Textkörper (HTML) der Startseite, ersetzt den Standard-Hero-Text."
    )
    startseite_bloecke: Optional[list[dict[str, Any]]] = Field(
        None,
        description="Abschnitte der Startseite als Liste von Blöcken (je mit 'id' und 'typ'). "
        "NULL = Standardaufbau.",
    )
    kontakt_email: Optional[str] = Field(
        None,
        description="Kontakt-E-Mail-Adresse für Freischaltungsanfragen bei der Registrierung.",
    )
    theme_color: Optional[str] = Field(
        None,
        description="Primärfarbe der Plattform als Hex-Code (z. B. '#507C96'). Leer = Standardfarbe.",
    )
    pdf_fusszeile_text: Optional[str] = Field(
        None,
        description="Hinweistext in der Fußzeile exportierter PDFs. Leer = keine Fußzeile; nie gesetzt = Standardtext.",
    )
    web_app_title: Optional[str] = Field(
        None,
        description="Titel der Anwendung (Browser-Tab-Titel). Leer = Standardtitel.",
    )

    @field_validator("startseite_bloecke")
    @classmethod
    def validate_startseite_bloecke(
        cls, value: Optional[list[dict[str, Any]]]
    ) -> Optional[list[dict[str, Any]]]:
        if value is None:
            return None
        if len(value) > STARTSEITE_MAX_BLOECKE:
            raise ValueError(f"Maximal {STARTSEITE_MAX_BLOECKE} Abschnitte erlaubt.")
        for block in value:
            if block.get("typ") not in STARTSEITE_BLOCK_TYPEN:
                raise ValueError(f"Unbekannter Abschnittstyp: {block.get('typ')!r}")
            if not isinstance(block.get("id"), str) or not block["id"]:
                raise ValueError("Jeder Abschnitt benötigt eine 'id'.")
        return value

    @field_validator("theme_color")
    @classmethod
    def validate_theme_color(cls, value: Optional[str]) -> Optional[str]:
        if value is None or value == "":
            return None
        if not re.match(HEX_COLOR_PATTERN, value):
            raise ValueError("theme_color muss ein Hex-Farbcode im Format '#RRGGBB' sein.")
        return value


class PlattformEinstellungUpdate(PlattformEinstellungBase):
    datenschutz_modus: Optional[RechtstextModus] = Field(None)
    impressum_modus: Optional[RechtstextModus] = Field(None)
    nutzungsbedingungen_modus: Optional[RechtstextModus] = Field(None)


class PlattformEinstellungRead(PlattformEinstellungBase):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the Plattform-Einstellung.")

    @field_validator("pdf_fusszeile_text")
    @classmethod
    def default_footer_text(cls, value: Optional[str]) -> str:
        # Never saved yet -> show (and print) the default text
        return DEFAULT_PDF_FOOTER_TEXT if value is None else value
