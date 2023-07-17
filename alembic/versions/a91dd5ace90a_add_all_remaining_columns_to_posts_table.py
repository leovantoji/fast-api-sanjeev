"""add all remaining columns to posts table

Revision ID: a91dd5ace90a
Revises: aecb95eb802e
Create Date: 2023-07-17 22:56:39.995303

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "a91dd5ace90a"
down_revision = "aecb95eb802e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        table_name="posts",
        column=sa.Column(
            "published", sa.Boolean(), nullable=False, server_default="TRUE"
        ),
    )
    op.add_column(
        table_name="posts",
        column=sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade() -> None:
    op.drop_column(table_name="posts", column_name="published")
    op.drop_column(table_name="posts", column_name="created_at")
