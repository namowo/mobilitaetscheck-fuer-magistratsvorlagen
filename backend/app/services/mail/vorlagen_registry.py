from pathlib import Path

TEMPLATE_FOLDER = Path(__file__).parent / "templates"

DEFAULT_VORLAGEN = {
    "account-bestaetigen": {
        "betreff": "Willkommen – bitte bestätigen Sie Ihren Account",
        "datei": "account-bestaetigen.html",
        "platzhalter": ["vorname", "nachname", "rolle", "gemeinde", "url"],
    },
    "einladung": {
        "betreff": "Einladung zur Registrierung beim Mobilitätscheck für Magistratsvorlagen",
        "datei": "einladung.html",
        "platzhalter": ["rolle", "gemeinde", "url", "gueltigkeitsdauer"],
    },
    "passwort-zuruecksetzen": {
        "betreff": "Passwort zurücksetzen",
        "datei": "passwort-zuruecksetzen.html",
        "platzhalter": ["vorname", "nachname", "url"],
    },
    "kommune-anfrage-politik": {
        "betreff": "Kommune für den Mobilitätscheck freischalten (Politik)",
        "datei": "kommune-anfrage-politik.txt",
        "platzhalter": [],
    },
    "kommune-anfrage-verwaltung": {
        "betreff": "Kommune für den Mobilitätscheck freischalten (Verwaltung)",
        "datei": "kommune-anfrage-verwaltung.txt",
        "platzhalter": [],
    },
}

TEXT_VORLAGEN = {"kommune-anfrage-politik", "kommune-anfrage-verwaltung"}


def get_default_inhalt(key: str) -> str:
    datei = DEFAULT_VORLAGEN[key]["datei"]
    return (TEMPLATE_FOLDER / datei).read_text(encoding="utf-8")
