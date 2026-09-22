"""add zeigt_kontakt_button to dokumentation_seite

Revision ID: a83265a838d8
Revises: 3c4a97b8d9f0
Create Date: 2026-09-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a83265a838d8'
down_revision: Union[str, None] = '3c4a97b8d9f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'dokumentation_seite',
        sa.Column(
            'zeigt_kontakt_button',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
            comment="Zeigt einen 'Kontakt aufnehmen'-Button unterhalb des Seiteninhalts an",
        ),
    )
    op.execute(
        "UPDATE dokumentation_seite SET zeigt_kontakt_button = true WHERE slug = 'kommune-hinzufuegen'"
    )


def downgrade() -> None:
    op.drop_column('dokumentation_seite', 'zeigt_kontakt_button')
