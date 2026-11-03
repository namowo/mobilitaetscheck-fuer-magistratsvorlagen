"""gemeinde: multiple verwaltung email domains

Revision ID: f3a4b5c6d7e8
Revises: e2f3a4b5c6d7
Create Date: 2026-11-03 00:00:00.000000
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "f3a4b5c6d7e8"
down_revision: Union[str, None] = "e2f3a4b5c6d7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "gemeinde",
        sa.Column(
            "verwaltung_email_domains",
            sa.ARRAY(sa.String()),
            nullable=False,
            server_default=sa.text("'{}'"),
            comment="Erlaubte E-Mail-Domains für Verwaltung-Benutzer (z.B. muenchen.de)",
        ),
    )
    op.execute(
        "UPDATE gemeinde SET verwaltung_email_domains = ARRAY[verwaltung_email_domain] "
        "WHERE verwaltung_email_domain IS NOT NULL AND verwaltung_email_domain <> ''"
    )
    op.drop_column("gemeinde", "verwaltung_email_domain")


def downgrade() -> None:
    op.add_column(
        "gemeinde",
        sa.Column("verwaltung_email_domain", sa.String(), nullable=True),
    )
    op.execute(
        "UPDATE gemeinde SET verwaltung_email_domain = verwaltung_email_domains[1] "
        "WHERE cardinality(verwaltung_email_domains) > 0"
    )
    op.drop_column("gemeinde", "verwaltung_email_domains")
