"""add startseite_titel and startseite_untertitel to plattform_einstellung

Revision ID: a3f9c1d2e4b7
Revises: f1a2b3c4d5e6
Create Date: 2026-09-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3f9c1d2e4b7'
down_revision: Union[str, None] = 'f1a2b3c4d5e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'startseite_titel',
            sa.Text(),
            nullable=True,
            comment='Titel des Hero-Bereichs der Startseite',
        ),
    )
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'startseite_untertitel',
            sa.Text(),
            nullable=True,
            comment='Untertitel des Hero-Bereichs der Startseite',
        ),
    )


def downgrade() -> None:
    op.drop_column('plattform_einstellung', 'startseite_untertitel')
    op.drop_column('plattform_einstellung', 'startseite_titel')
