import datetime
from fpdf import FPDF
from PIL import Image
from os import path

from app.core.config import DEFAULT_PDF_FOOTER_TEXT, settings


def gemeinde_logo_dir() -> str:
    return path.abspath(settings.GEMEINDE_LOGO_UPLOAD_DIR)


def resolve_gemeinde_logo_path(pdf_logo_dateiname: str | None) -> str | None:
    """Path to a Gemeinde's own PDF logo, or None if it has none (or the file is gone)."""
    if not pdf_logo_dateiname:
        return None
    # basename only: the value comes from the DB but must never escape the upload dir
    candidate = path.join(gemeinde_logo_dir(), path.basename(pdf_logo_dateiname))
    return candidate if path.isfile(candidate) else None


# Header geometry shared by all PDFs. The logo is scaled to fit this box
# (aspect ratio preserved), so it can never grow into the page content.
LOGO_X = 10
LOGO_Y = 8
LOGO_MAX_W = 40
LOGO_MAX_H = 10
HEADER_BOTTOM = LOGO_Y + LOGO_MAX_H + 4  # content always starts below this


class BasePDF(FPDF):

    def __init__(
        self, orientation="P", unit="mm", format="A4", logo_path=None, footer_text=None
    ):
        # Pass the parameters to FPDF's __init__ method
        super().__init__(orientation, unit, format)
        # Gemeinde logo if it has one; otherwise no logo is drawn
        self.logo_path = logo_path
        # Platform-configured footer attribution; None = built-in default, "" = no footer
        self.footer_text = footer_text
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

    def draw_logo(self):
        """Draw the Gemeinde logo scaled to fit LOGO_MAX_W x LOGO_MAX_H, top-left aligned.
        Draws nothing if the Gemeinde has not uploaded a logo."""
        if not self.logo_path:
            return
        try:
            logo = self.logo_path
            with Image.open(logo) as img:
                px_w, px_h = img.size
            scale = min(LOGO_MAX_W / px_w, LOGO_MAX_H / px_h)
            self.image(logo, x=LOGO_X, y=LOGO_Y, w=px_w * scale, h=px_h * scale)
        except Exception as e:
            print(e)

    FOOTER_MAX_LINES = 3
    FOOTER_LINE_H = 3.2
    FOOTER_BOTTOM_GAP = 3  # mm between the last line and the page edge
    PAGE_NUMBER_H = 4

    def _footer_lines(self) -> list[str]:
        """Attribution wrapped to the full content width, at most FOOTER_MAX_LINES lines."""
        # None = use the default; "" = Systemadmin turned the footer off
        text = DEFAULT_PDF_FOOTER_TEXT if self.footer_text is None else self.footer_text
        if not text:
            return []
        self.set_font("free-sans", "", 7)
        max_w = self.w - self.l_margin - self.r_margin

        lines: list[str] = []
        for paragraph in text.splitlines() or [text]:
            line = ""
            for word in paragraph.split():
                candidate = f"{line} {word}".strip()
                if line and self.get_string_width(candidate) > max_w:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            lines.append(line)
        lines = [ln for ln in lines if ln]
        truncated = len(lines) > self.FOOTER_MAX_LINES
        lines = lines[: self.FOOTER_MAX_LINES]
        if truncated:
            lines[-1] = lines[-1].rstrip(".") + " …"
        result = []
        for ln in lines:
            while len(ln) > 1 and self.get_string_width(ln) > max_w:
                ln = ln[:-2].rstrip() + "…"
            result.append(ln)
        return result

    def footer_block_height(self) -> float:
        """Height of the page-number + attribution block at the bottom of every page."""
        n = len(self._footer_lines())
        gap = 1 if n else 0
        return (
            self.FOOTER_BOTTOM_GAP + n * self.FOOTER_LINE_H + gap + self.PAGE_NUMBER_H
        )

    def draw_page_footer(self, number_color=(0, 0, 0)):
        """Centred 'Seite x/y', with the attribution underneath across the full page width."""
        lines = self._footer_lines()
        top = self.h - self.footer_block_height()
        width = self.w - self.l_margin - self.r_margin
        saved_color = self.text_color

        self.set_xy(self.l_margin, top)
        self.set_font("free-sans", "", 8)
        self.set_text_color(*number_color)
        self.cell(width, self.PAGE_NUMBER_H, f"Seite {self.page_no()}/{{nb}}", align="C")

        self.set_font("free-sans", "", 7)
        self.set_text_color(107, 114, 128)
        for i, ln in enumerate(lines):
            self.set_xy(
                self.l_margin, top + self.PAGE_NUMBER_H + 1 + i * self.FOOTER_LINE_H
            )
            self.cell(width, self.FOOTER_LINE_H, ln, align="C")
        self.text_color = saved_color

    def header(self):
        self.draw_logo()
        self.set_font("free-sans", "", 10)
        self.set_xy(self.l_margin, LOGO_Y)
        self.cell(0, 8, f"{datetime.date.today().strftime('%d.%m.%Y')}", align="R")
        self.set_y(HEADER_BOTTOM)
