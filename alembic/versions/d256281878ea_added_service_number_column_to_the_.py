"""Added service number column to the employee records model class and removed null=True constraints from some columns.

Revision ID: d256281878ea
Revises: 03a5ffec4e8f
Create Date: 2025-10-06 17:08:24.466253
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d256281878ea"
down_revision: Union[str, Sequence[str], None] = "03a5ffec4e8f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("employee_records", recreate="always") as batch_op:
        batch_op.add_column(sa.Column("service_number", sa.String(), nullable=False))
        batch_op.alter_column("unit", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.alter_column("grade", existing_type=sa.VARCHAR(), nullable=False)
        batch_op.create_index("ix_employee_records_service_number", ["service_number"])


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("employee_records", recreate="always") as batch_op:
        batch_op.drop_index("ix_employee_records_service_number")
        batch_op.drop_column("service_number")
        batch_op.alter_column("unit", existing_type=sa.VARCHAR(), nullable=True)
        batch_op.alter_column("grade", existing_type=sa.VARCHAR(), nullable=True)
