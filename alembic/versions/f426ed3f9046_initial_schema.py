"""initial schema

Revision ID: f426ed3f9046
Revises: 
Create Date: 2026-03-30 16:38:16.087050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = 'f426ed3f9046'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # addresses (pas de FK, créée en premier)
    op.create_table('addresses',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('box_number', sa.String(), nullable=False),
        sa.Column('street', sa.String(), nullable=False),
        sa.Column('post_name', sa.String(), nullable=False),
        sa.Column('post_code', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
    )

    # organizations (self-referencing FK, parent_id nullable)
    op.create_table('organizations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('acronym', sa.String(), nullable=True),
        sa.Column('logo', sa.String(), nullable=True),
        sa.Column('purpose', sa.String(), nullable=False),
        sa.Column('org_type', sa.String(), nullable=False),
        sa.Column('sgp_type', sa.String(), nullable=True),
        sa.Column('billable', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_legal_entity', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('parent_id', UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=True),
    )

    # users (FK vers addresses)
    op.create_table('users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('first_names', sa.JSON(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('gender', sa.String(), nullable=True),
        sa.Column('totem', sa.String(), nullable=True),
        sa.Column('quali', sa.String(), nullable=True),
        sa.Column('is_legal_guardian', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('home_address_id', UUID(as_uuid=True), sa.ForeignKey('addresses.id'), nullable=False),
        sa.Column('residential_address_id', UUID(as_uuid=True), sa.ForeignKey('addresses.id'), nullable=True),
    )

    # memberships (FK vers users + organizations)
    op.create_table('memberships',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('organization_id', UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('price', sa.Numeric(10, 2), nullable=True),
    )

    # contacts (FK vers users + organizations)
    op.create_table('contacts',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.String(), nullable=True),
        sa.Column('website', sa.String(), nullable=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('org_id', UUID(as_uuid=True), sa.ForeignKey('organizations.id', ondelete='CASCADE'), nullable=True),
    )

    # audiences
    op.create_table('audiences',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('label', sa.String(), nullable=False, unique=True),
    )

    # events (self-referencing FK)
    op.create_table('events',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('event_type', sa.String(), nullable=False),
        sa.Column('start_date', sa.DateTime(), nullable=True),
        sa.Column('end_date', sa.DateTime(), nullable=True),
        sa.Column('latitude', sa.Float(), nullable=True),
        sa.Column('longitude', sa.Float(), nullable=True),
        sa.Column('parent_id', UUID(as_uuid=True), sa.ForeignKey('events.id'), nullable=True),
    )

    # event_audience (table d'association N-N)
    op.create_table('event_audience',
        sa.Column('event_id', UUID(as_uuid=True), sa.ForeignKey('events.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('audience_id', UUID(as_uuid=True), sa.ForeignKey('audiences.id', ondelete='CASCADE'), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table('event_audience')
    op.drop_table('events')
    op.drop_table('audiences')
    op.drop_table('contacts')
    op.drop_table('memberships')
    op.drop_table('users')
    op.drop_table('organizations')
    op.drop_table('addresses')