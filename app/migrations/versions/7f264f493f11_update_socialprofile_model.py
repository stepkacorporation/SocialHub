"""Update SocialProfile model

Revision ID: 7f264f493f11
Revises: e4541d79bb32
Create Date: 2024-08-23 00:37:19.854527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f264f493f11'
down_revision: Union[str, None] = 'e4541d79bb32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('social_profiles', sa.Column('platform', sa.String(), nullable=False))
    op.add_column('social_profiles', sa.Column('profile_type', sa.String(), nullable=False))
    op.drop_column('social_profiles', 'platform_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('social_profiles', sa.Column('platform_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('social_profiles', 'profile_type')
    op.drop_column('social_profiles', 'platform')
    # ### end Alembic commands ###
