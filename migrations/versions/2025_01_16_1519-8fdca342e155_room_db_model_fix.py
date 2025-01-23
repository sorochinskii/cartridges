"""Room db model fix

Revision ID: 8fdca342e155
Revises: d45d33e62359
Create Date: 2025-01-16 15:19:25.381420

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fdca342e155'
down_revision: Union[str, None] = 'd45d33e62359'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'building', ['id'])
    op.alter_column('room', 'building_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_unique_constraint(None, 'room', ['id'])
    op.create_foreign_key(None, 'room', 'building', ['building_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'room', type_='foreignkey')
    op.drop_constraint(None, 'room', type_='unique')
    op.alter_column('room', 'building_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint(None, 'building', type_='unique')
    # ### end Alembic commands ###
