"""add pdf_fusszeile_text to plattform_einstellung

Revision ID: b6c7d8e9f0a1
Revises: a4b5c6d7e8f9
Create Date: 2026-11-03 00:00:00.000000
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "b6c7d8e9f0a1"
down_revision: Union[str, None] = "a4b5c6d7e8f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "plattform_einstellung",
        sa.Column(
            "pdf_fusszeile_text",
            sa.Text(),
            nullable=True,
            comment="Hinweistext in der Fußzeile exportierter PDFs. Leer = Standardtext.",
        ),
    )


def downgrade() -> None:
    op.drop_column("plattform_einstellung", "pdf_fusszeile_text")
