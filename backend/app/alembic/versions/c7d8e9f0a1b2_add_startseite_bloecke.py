"""add startseite_bloecke to plattform_einstellung for a section-based homepage

Revision ID: c7d8e9f0a1b2
Revises: b6c7d8e9f0a1
Create Date: 2026-11-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'c7d8e9f0a1b2'
down_revision: Union[str, None] = 'b6c7d8e9f0a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'plattform_einstellung',
        sa.Column(
            'startseite_bloecke',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
            comment='Abschnitte der Startseite (Liste von Blöcken). NULL = Standardaufbau.',
        ),
    )


def downgrade() -> None:
    op.drop_column('plattform_einstellung', 'startseite_bloecke')
