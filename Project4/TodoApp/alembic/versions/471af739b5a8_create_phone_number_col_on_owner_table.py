"""create phone number col on owner table

Revision ID: 471af739b5a8
Revises:
Create Date: 2025-11-03 20:13:18.268182

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "471af739b5a8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("owner", sa.Column("phone_number", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("owner", "phone_number")
