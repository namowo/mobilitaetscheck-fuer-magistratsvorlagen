"""add is_local_superuser to user

Revision ID: 0085b0a8c141
Revises: a83265a838d8
Create Date: 2026-09-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0085b0a8c141'
down_revision: Union[str, None] = 'a83265a838d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'user',
        sa.Column(
            'is_local_superuser',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
            comment='Gemeinde-Admin: Adminrechte innerhalb der eigenen Gemeinde (unabhängig von is_superuser, das nur Plattform-Administratoren vorbehalten ist)',
        ),
    )

    # Existing Gemeinde Admins were modeled as "Verwaltung role + is_superuser=True".
    # Migrate them to the new explicit is_local_superuser flag, and reserve
    # is_superuser exclusively for Platform Admins (Admin role) going forward.
    op.execute(
        """
        UPDATE "user"
        SET is_local_superuser = true
        FROM user_rolle
        WHERE "user".rolle_id = user_rolle.id
          AND user_rolle.name = 'Verwaltung'
          AND "user".is_superuser = true
        """
    )
    op.execute(
        """
        UPDATE "user"
        SET is_superuser = false
        FROM user_rolle
        WHERE "user".rolle_id = user_rolle.id
          AND user_rolle.name = 'Verwaltung'
          AND "user".is_superuser = true
        """
    )


def downgrade() -> None:
    op.execute(
        """
        UPDATE "user"
        SET is_superuser = true
        WHERE is_local_superuser = true
        """
    )
    op.drop_column('user', 'is_local_superuser')
