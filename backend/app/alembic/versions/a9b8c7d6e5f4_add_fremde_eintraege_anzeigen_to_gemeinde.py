"""add fremde_*_anzeigen and inhalte_teilen to gemeinde

Revision ID: a9b8c7d6e5f4
Revises: c7d8e9f0a1b2
Create Date: 2026-11-19 00:00:00.000000
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "a9b8c7d6e5f4"
down_revision: Union[str, None] = "c7d8e9f0a1b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

SPALTEN = {
    "fremde_tags_anzeigen": "Für andere Kommunen sichtbare Tags in dieser Gemeinde anzeigen",
    "fremde_indikatoren_anzeigen": "Für andere Kommunen sichtbare Indikatoren in dieser Gemeinde anzeigen",
    "fremde_textbausteine_anzeigen": "Für andere Kommunen sichtbare Textbausteine in dieser Gemeinde anzeigen",
    "inhalte_teilen": "Nutzer:innen dürfen Tags, Indikatoren und Textbausteine mit anderen Kommunen teilen",
}


def upgrade() -> None:
    for name, comment in SPALTEN.items():
        op.add_column(
            "gemeinde",
            sa.Column(
                name,
                sa.Boolean(),
                nullable=False,
                server_default=sa.true(),
                comment=comment,
            ),
        )


def downgrade() -> None:
    for name in SPALTEN:
        op.drop_column("gemeinde", name)
