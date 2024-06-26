"""empty message

Revision ID: 48593ba7298d
Revises: fa9fed151ce1
Create Date: 2024-04-06 18:30:42.269938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48593ba7298d'
down_revision = 'fa9fed151ce1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('friends', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Enum('PENDING', 'ACCEPTED', 'REJECTED', name='enumstatus'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('friends', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
