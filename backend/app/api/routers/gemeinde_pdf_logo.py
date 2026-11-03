import io
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from PIL import Image, UnidentifiedImageError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import current_active_user, get_async_session
from app.models.gemeinde import Gemeinde
from app.models.user import User
from app.schemas.gemeinde import GemeindeRead
from app.services.pdf.base_pdf import gemeinde_logo_dir, resolve_gemeinde_logo_path

router = APIRouter()

MAX_LOGO_BYTES = 2 * 1024 * 1024  # 2 MB
MAX_LOGO_PIXELS = 4000  # per side; guards against decompression bombs
FORMAT_TO_EXTENSION = {"PNG": ("png", "image/png"), "JPEG": ("jpg", "image/jpeg")}


def _delete_file(dateiname: str | None) -> None:
    if dateiname:
        (Path(gemeinde_logo_dir()) / Path(dateiname).name).unlink(missing_ok=True)


async def current_logo_editor(user: User = Depends(current_active_user)) -> User:
    """Only kommunale Administrator:innen (local superusers) may change their Gemeinde's logo."""
    if not user.is_local_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Keine Berechtigung")
    return user


@router.get("")
async def get_pdf_logo(user: User = Depends(current_active_user)):
    """The logo of the current user's Gemeinde (used for the preview in Einstellungen)."""
    logo_path = resolve_gemeinde_logo_path(user.gemeinde.pdf_logo_dateiname)
    if logo_path is None:
        raise HTTPException(status_code=404, detail="Kein Logo hinterlegt.")
    return FileResponse(logo_path, headers={"Cache-Control": "no-cache"})


@router.put("", response_model=GemeindeRead)
async def upload_pdf_logo(
    file: UploadFile,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_logo_editor),
):
    contents = await file.read(MAX_LOGO_BYTES + 1)
    if len(contents) > MAX_LOGO_BYTES:
        raise HTTPException(status_code=400, detail="Datei ist zu groß (max. 2 MB).")

    # Trust the actual image data, not the client-supplied content type.
    try:
        with Image.open(io.BytesIO(contents)) as img:
            img_format = img.format
            width, height = img.size
            img.verify()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Die Datei ist kein gültiges Bild.")
    if img_format not in FORMAT_TO_EXTENSION:
        raise HTTPException(
            status_code=400, detail="Nur PNG- und JPEG-Dateien sind erlaubt."
        )
    if width > MAX_LOGO_PIXELS or height > MAX_LOGO_PIXELS or width < 1 or height < 1:
        raise HTTPException(
            status_code=400,
            detail=f"Das Bild ist zu groß (max. {MAX_LOGO_PIXELS}x{MAX_LOGO_PIXELS} Pixel).",
        )

    extension = FORMAT_TO_EXTENSION[img_format][0]
    dateiname = f"{user.gemeinde_id}-{uuid.uuid4().hex[:8]}.{extension}"
    Path(gemeinde_logo_dir()).mkdir(parents=True, exist_ok=True)
    (Path(gemeinde_logo_dir()) / dateiname).write_bytes(contents)

    gemeinde = await db.get(Gemeinde, user.gemeinde_id)
    old = gemeinde.pdf_logo_dateiname
    gemeinde.pdf_logo_dateiname = dateiname
    await db.commit()
    await db.refresh(gemeinde)
    _delete_file(old)
    return gemeinde


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pdf_logo(
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_logo_editor),
):
    gemeinde = await db.get(Gemeinde, user.gemeinde_id)
    old = gemeinde.pdf_logo_dateiname
    gemeinde.pdf_logo_dateiname = None
    await db.commit()
    _delete_file(old)
