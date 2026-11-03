"""add pdf_logo_dateiname to gemeinde

Revision ID: a4b5c6d7e8f9
Revises: f3a4b5c6d7e8
Create Date: 2026-11-03 00:00:00.000000
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "a4b5c6d7e8f9"
down_revision: Union[str, None] = "f3a4b5c6d7e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "gemeinde",
        sa.Column(
            "pdf_logo_dateiname",
            sa.String(),
            nullable=True,
            comment="Dateiname des Kommunen-Logos für PDF-Exporte (in GEMEINDE_LOGO_UPLOAD_DIR)",
        ),
    )


def downgrade() -> None:
    op.drop_column("gemeinde", "pdf_logo_dateiname")
