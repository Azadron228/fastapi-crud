"""empty message

Revision ID: 2c275745ff43
Revises: 1a57213df53b
Create Date: 2024-07-15 14:25:41.551396

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2c275745ff43'
down_revision: Union[str, None] = '1a57213df53b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'some_field')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('some_field', postgresql.ENUM('pending', 'completed', 'cancelled', name='orderstatus', create_type=False), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
