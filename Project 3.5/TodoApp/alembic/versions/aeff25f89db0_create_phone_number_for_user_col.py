"""create phone number for owner col

Revision ID: aeff25f89db0
Revises:
Create Date: 2023-08-28 19:59:25.616334

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "aeff25f89db0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("owner", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("owner", "phone_number")
