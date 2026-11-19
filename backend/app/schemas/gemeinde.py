import re
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, computed_field, field_validator

DOMAIN_RE = re.compile(r"^[a-z0-9.-]+\.[a-z]{2,}$")


def _normalize_domains(value):
    if value is None:
        return value
    domains = []
    for d in value:
        d = d.strip().lower().lstrip("@")
        if not DOMAIN_RE.match(d):
            raise ValueError(f"Ungültige Domain: {d}")
        if d not in domains:
            domains.append(d)
    return domains


class GemeindeBase(BaseModel):
    """
    Base schema for a Gemeinde, containing the primary name attribute.
    """

    name: str = Field(..., description="The name of the Gemeinde.")
    verwaltung_email_domains: List[str] = Field(default_factory=list, description="Erlaubte E-Mail-Domains für Verwaltung-Benutzer (z.B. muenchen.de).")

    _norm = field_validator("verwaltung_email_domains")(_normalize_domains)


class GemeindeCreate(GemeindeBase):
    """
    Schema for creating a new Gemeinde. Inherits fields from GemeindeBase.
    """

    klimacheck_aktiv: bool = Field(False, description="Klimacheck für die Gemeinde aktivieren.")


class GemeindeUpdate(BaseModel):
    """
    Schema for updating an existing Gemeinde. Allows partial updates.
    """

    name: Optional[str] = Field(None, description="The updated name of the Gemeinde.")
    verwaltung_email_domains: Optional[List[str]] = Field(None, description="Erlaubte E-Mail-Domains für Verwaltung-Benutzer.")

    _norm = field_validator("verwaltung_email_domains")(_normalize_domains)
    klimacheck_aktiv: Optional[bool] = Field(None, description="Klimacheck für die Gemeinde aktivieren/deaktivieren.")


class GemeindeRead(GemeindeBase):
    """
    Read schema for a Gemeinde, including the unique identifier.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for the Gemeinde.")
    standard_ziel_set_id: Optional[int] = Field(None, description="ID des Standard-Leitziele-Sets.")
    klimacheck_aktiv: bool = Field(False, description="Ob der Klimacheck für die Gemeinde aktiviert ist.")
    fremde_tags_anzeigen: bool = Field(True, description="Tags anderer Kommunen anzeigen.")
    fremde_indikatoren_anzeigen: bool = Field(True, description="Indikatoren anderer Kommunen anzeigen.")
    fremde_textbausteine_anzeigen: bool = Field(True, description="Textbausteine anderer Kommunen anzeigen.")
    inhalte_teilen: bool = Field(True, description="Teilen eigener Inhalte mit anderen Kommunen erlaubt.")
    pdf_logo_dateiname: Optional[str] = Field(None, exclude=True)

    @computed_field
    @property
    def hat_pdf_logo(self) -> bool:
        return bool(self.pdf_logo_dateiname)


class GemeindeFremdeEintraegeRead(BaseModel):
    """
    Kommunale Einstellungen: ob für andere Kommunen sichtbare Einträge angezeigt werden.
    """

    model_config = ConfigDict(from_attributes=True)

    fremde_tags_anzeigen: bool
    fremde_indikatoren_anzeigen: bool
    fremde_textbausteine_anzeigen: bool
    inhalte_teilen: bool


class GemeindeFremdeEintraegeUpdate(BaseModel):
    """
    Partial update der kommunalen Einstellungen zu Einträgen anderer Kommunen.
    """

    fremde_tags_anzeigen: Optional[bool] = None
    fremde_indikatoren_anzeigen: Optional[bool] = None
    fremde_textbausteine_anzeigen: Optional[bool] = None
    inhalte_teilen: Optional[bool] = None
