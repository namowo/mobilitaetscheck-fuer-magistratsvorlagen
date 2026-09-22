"""add kontakt_email to plattform_einstellung

Revision ID: b5c6d7e8f9a0
Revises: a3f9c1d2e4b7
Create Date: 2026-09-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5c6d7e8f9a0'
down_revision: Union[str, None] = 'a3f9c1d2e4b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'kontakt_email',
            sa.Text(),
            nullable=True,
            comment='Kontakt-E-Mail-Adresse für Freischaltungsanfragen bei der Registrierung',
        ),
    )


def downgrade() -> None:
    op.drop_column('plattform_einstellung', 'kontakt_email')
