"""add theme_color to plattform_einstellung

Revision ID: c6d7e8f9a0b1
Revises: b5c6d7e8f9a0
Create Date: 2026-09-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6d7e8f9a0b1'
down_revision: Union[str, None] = 'b5c6d7e8f9a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'theme_color',
            sa.Text(),
            nullable=True,
            comment="Primärfarbe der Plattform als Hex-Code (z. B. '#507C96'). Leer = Standardfarbe.",
        ),
    )


def downgrade() -> None:
    op.drop_column('plattform_einstellung', 'theme_color')
