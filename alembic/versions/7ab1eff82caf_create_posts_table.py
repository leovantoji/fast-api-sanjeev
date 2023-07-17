"""create posts table

Revision ID: 7ab1eff82caf
Revises:
Create Date: 2023-07-17 18:00:38.330547

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "7ab1eff82caf"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("posts")
