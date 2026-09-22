import datetime
import os
import shutil
from fpdf import FPDF
from os import path

from app.core.config import settings


ACTIVE_LOGO_BASENAME = "active"


def _active_logo_dir() -> str:
    return path.abspath(settings.PDF_LOGO_UPLOAD_DIR)


def sync_active_pdf_logo(source_path: str | None) -> None:
    """Mirror the branding asset assigned to the 'pdf-logo' slot into a local cache file
    that resolve_logo_path() can read synchronously (PDF rendering can't await a DB call).
    Pass None to clear it (falls back to the bundled default logo)."""
    active_dir = _active_logo_dir()
    if os.path.isdir(active_dir):
        for f in os.listdir(active_dir):
            if path.splitext(f)[0] == ACTIVE_LOGO_BASENAME:
                os.remove(path.join(active_dir, f))

    if source_path is None:
        return

    os.makedirs(active_dir, exist_ok=True)
    extension = path.splitext(source_path)[1]
    shutil.copyfile(source_path, path.join(active_dir, f"{ACTIVE_LOGO_BASENAME}{extension}"))


def resolve_logo_path() -> str:
    """Path to the active PDF logo: the admin-selected branding asset if present, else the bundled default."""
    active_dir = _active_logo_dir()
    if os.path.isdir(active_dir):
        for f in os.listdir(active_dir):
            if path.splitext(f)[0] == ACTIVE_LOGO_BASENAME:
                return path.join(active_dir, f)

    script_dir = path.dirname(path.abspath(__file__))
    return path.normpath(path.join(script_dir, "./assests/pimoo-logo.png"))


class BasePDF(FPDF):

    def __init__(self, orientation="P", unit="mm", format="A4"):
        # Pass the parameters to FPDF's __init__ method
        super().__init__(orientation, unit, format)
        font_path = path.dirname(path.abspath(__file__))
        self.add_font(
            "free-sans",
            style="",
            fname=path.join(font_path, "./assests/FreeSans/FreeSans.ttf"),
        )
        self.add_font(
            "free-sans",
            style="b",
            fname=path.join(font_path, "./assests/FreeSans/FreeSansBold.ttf"),
        )
        self.add_font(
            "free-sans",
            style="i",
            fname=path.join(font_path, "./assests/FreeSans/FreeSansOblique.ttf"),
        )
        self.add_font(
            "free-sans",
            style="bi",
            fname=path.join(font_path, "./assests/FreeSans/FreeSansBoldOblique.ttf"),
        )

    def header(self):
        try:
            self.image(resolve_logo_path(), 10, 8, 30)
        except Exception as e:
            print(e)
        self.set_font("free-sans", "", 10)
        self.cell(0, 8, f"{datetime.date.today().strftime('%d.%m.%Y')}", align="R")
        self.ln(15)
