"""Model rename to CartridgeModel

Revision ID: 9af17443eecc
Revises: 5ee7811ec0cc
Create Date: 2025-09-19 15:12:34.697337

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9af17443eecc"
down_revision: Union[str, None] = "5ee7811ec0cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("model_original_id_fkey", "model", type_="foreignkey")
    op.rename_table("model", "cartridge_model")
    op.create_foreign_key(
        "cartridge_model_original_id_fkey",
        "cartridge_model",
        "cartridge_model",
        ["original_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "cartridge_model_original_id_fkey",
        "cartridge_model",
        type_="foreignkey",
    )
    op.rename_table("cartridge_model", "model")
    op.create_foreign_key(
        "model_original_id_fkey", "model", "model", ["original_id"], ["id"]
    )
