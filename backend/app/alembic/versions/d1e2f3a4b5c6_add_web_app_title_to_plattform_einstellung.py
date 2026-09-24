"""add web_app_title to plattform_einstellung

Revision ID: d1e2f3a4b5c6
Revises: 0085b0a8c141
Create Date: 2026-09-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1e2f3a4b5c6'
down_revision: Union[str, None] = '0085b0a8c141'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'web_app_title',
            sa.Text(),
            nullable=True,
            comment="Titel der Anwendung (Browser-Tab-Titel). Leer = Standardtitel.",
        ),
    )


def downgrade() -> None:
    op.drop_column('plattform_einstellung', 'web_app_title')
