"""ajout nationalite pour les utilisateurs

Revision ID: 2cebbed2a995
Revises: 4a0aa8d83698
Create Date: 2026-04-16 10:01:02.523071
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cebbed2a995'
down_revision: Union[str, Sequence[str], None] = '4a0aa8d83698'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # 1. Ajouter la colonne
    op.add_column(
        'users',
        sa.Column('nationality', sa.JSON(), nullable=True)
    )

    # 2. Valeur par défaut métier
    op.execute("UPDATE users SET nationality = '[\"BE\"]'")

    # 3. Rendre NOT NULL
    op.alter_column(
        'users',
        'nationality',
        nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'nationality')