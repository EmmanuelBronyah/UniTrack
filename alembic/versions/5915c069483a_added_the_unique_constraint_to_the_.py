"""Added the unique constraint to the service number column.

Revision ID: 5915c069483a
Revises: d256281878ea
Create Date: 2025-10-08 12:50:45.501109

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5915c069483a"
down_revision: Union[str, Sequence[str], None] = "d256281878ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing index on service_number (if any)
    op.drop_index(
        op.f("ix_employee_records_service_number"), table_name="employee_records"
    )

    # Recreate the table schema to apply both changes
    with op.batch_alter_table("employee_records", schema=None) as batch_op:
        batch_op.alter_column(
            "appointment_date",
            existing_type=sa.DATETIME(),
            type_=sa.Date(),
            existing_nullable=True,
        )
        batch_op.create_index(
            op.f("ix_employee_records_service_number"),
            ["service_number"],
            unique=True,
        )


def downgrade() -> None:
    with op.batch_alter_table("employee_records", schema=None) as batch_op:
        batch_op.alter_column(
            "appointment_date",
            existing_type=sa.Date(),
            type_=sa.DATETIME(),
            existing_nullable=True,
        )
        batch_op.drop_index(op.f("ix_employee_records_service_number"))
        batch_op.create_index(
            op.f("ix_employee_records_service_number"),
            ["service_number"],
            unique=False,
        )
