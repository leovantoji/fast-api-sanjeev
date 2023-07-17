"""add content column to posts table

Revision ID: 55326af21e7f
Revises: 7ab1eff82caf
Create Date: 2023-07-17 22:39:57.942893

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "55326af21e7f"
down_revision = "7ab1eff82caf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column(
        table_name="posts",
        column_name="content",
    )
