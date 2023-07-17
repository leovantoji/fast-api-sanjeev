"""add foreign key to posts table

Revision ID: aecb95eb802e
Revises: dca9f83b39a5
Create Date: 2023-07-17 22:53:02.123431

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "aecb95eb802e"
down_revision = "dca9f83b39a5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))

    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(constraint_name="posts_users_fk", table_name="posts")
    op.drop_column(table_name="posts", column_name="owner_id")
