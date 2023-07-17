"""add users table

Revision ID: dca9f83b39a5
Revises: 55326af21e7f
Create Date: 2023-07-17 22:47:56.061705

"""
import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = "dca9f83b39a5"
down_revision = "55326af21e7f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("email", sa.String(), nullable=False, unique=True),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
