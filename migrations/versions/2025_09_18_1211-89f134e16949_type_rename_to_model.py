"""Type rename to Model

Revision ID: 89f134e16949
Revises: 1bf8265fba47
Create Date: 2025-09-18 12:11:59.593753

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "89f134e16949"
down_revision: Union[str, None] = "1bf8265fba47"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("type_original_id_fkey", "type", type_="foreignkey")
    op.rename_table("type", "model")
    op.create_foreign_key(
        "model_original_id_fkey", "model", "model", ["original_id"], ["id"]
    )


def downgrade() -> None:
    op.drop_constraint("model_original_id_fkey", "model", type_="foreignkey")
    op.rename_table("model", "type")
    op.create_foreign_key(
        "type_original_id_fkey", "type", "type", ["original_id"], ["id"]
    )
