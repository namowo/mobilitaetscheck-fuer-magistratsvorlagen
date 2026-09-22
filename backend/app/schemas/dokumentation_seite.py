from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class DokumentationSeiteBase(BaseModel):
    """
    Base schema for a documentation page, containing title and content.
    """

    titel: str = Field(..., description="Titel der Dokumentationsseite")
    slug: str = Field(..., description="Eindeutiger Anker-Slug der Seite")
    inhalt: Optional[str] = Field(None, description="Rich-Text-Inhalt der Dokumentationsseite (HTML)")
    zeigt_kontakt_button: bool = Field(
        False,
        description="Zeigt einen 'Kontakt aufnehmen'-Button unterhalb des Seiteninhalts an",
    )


class DokumentationSeiteCreate(DokumentationSeiteBase):
    """
    Schema for creating a new documentation page. Inherits fields from DokumentationSeiteBase.
    """

    pass


class DokumentationSeiteUpdate(BaseModel):
    """
    Schema for updating an existing documentation page, allowing partial updates.
    """

    titel: Optional[str] = Field(None, description="Neuer Titel der Dokumentationsseite")
    slug: Optional[str] = Field(None, description="Neuer Anker-Slug der Seite")
    inhalt: Optional[str] = Field(None, description="Neuer Rich-Text-Inhalt der Dokumentationsseite (HTML)")
    zeigt_kontakt_button: Optional[bool] = Field(
        None, description="Neuer Status des 'Kontakt aufnehmen'-Buttons"
    )


class DokumentationSeiteRead(DokumentationSeiteBase):
    """
    Read schema for a documentation page, including metadata fields.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Eindeutige ID der Dokumentationsseite.")
    reihenfolge: int = Field(..., description="Anzeigereihenfolge der Seite.")


class DokumentationSeiteReorderItem(BaseModel):
    id: int = Field(..., description="ID der Dokumentationsseite.")
    reihenfolge: int = Field(..., description="Neue Anzeigereihenfolge.")


class DokumentationSeiteReorderUpdate(BaseModel):
    reihenfolge: list[DokumentationSeiteReorderItem] = Field(
        ..., description="Neue Reihenfolge aller Dokumentationsseiten."
    )
