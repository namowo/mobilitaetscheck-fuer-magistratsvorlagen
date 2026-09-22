from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.future import select

from app.core.config import settings
from app.core.db import async_session_maker
from app.crud.exceptions import AuthorizationError, DatabaseCommitError, NotFoundError
from app.exceptions import (
    authorization_exception_handler,
    database_commit_exception_handler,
    not_found_exception_handler,
)
from app.api.main import router
from app.api.routers.frontend import SPAStaticFiles

# Imported after app.api.main (which imports app.core.deps first) so that fastapi_users'
# optional-dependency import guards resolve in the same order the running app always uses.
from app.crud.branding_bild import PDF_LOGO_SLOT
from app.models.branding_slot_zuweisung import BrandingSlotZuweisung
from app.services.pdf.base_pdf import sync_active_pdf_logo


description = """
This is a fancy API built with [FastAPI🚀](https://fastapi.tiangolo.com/)

📝 [Source Code](https://github.com/johanngrobe/stellplatztool-backend)  
🐞 [Issues](https://github.com/johanngrobe/stellplatztool-backend/issues) 
"""


app = FastAPI(
    title="API Mobilitätscheck für Magistratsvorlagen",
    description=description,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

app.add_exception_handler(AuthorizationError, authorization_exception_handler)
app.add_exception_handler(DatabaseCommitError, database_commit_exception_handler)
app.add_exception_handler(NotFoundError, not_found_exception_handler)

app.include_router(router, prefix=settings.API_V1_STR)

Path(settings.BRANDING_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
app.mount(
    "/uploads/branding",
    StaticFiles(directory=settings.BRANDING_UPLOAD_DIR),
    name="branding-uploads",
)


@app.on_event("startup")
async def resync_active_pdf_logo() -> None:
    """Rebuild the local PDF-logo render cache from the DB-assigned branding asset,
    in case the cache directory was reset (redeploy, ephemeral disk, ...)."""
    async with async_session_maker() as db:
        result = await db.execute(
            select(BrandingSlotZuweisung).where(BrandingSlotZuweisung.slot == PDF_LOGO_SLOT)
        )
        zuweisung = result.scalar_one_or_none()
        if zuweisung and zuweisung.asset_id and zuweisung.asset:
            sync_active_pdf_logo(str(Path(settings.BRANDING_UPLOAD_DIR) / zuweisung.asset.dateiname))
        else:
            sync_active_pdf_logo(None)


app.mount(
    "/",
    SPAStaticFiles(directory=settings.FRONTEND_DIR, html=True),
    name="frontend",
)
