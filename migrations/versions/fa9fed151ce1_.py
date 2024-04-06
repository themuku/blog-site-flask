"""empty message

Revision ID: fa9fed151ce1
Revises: 288edd42bc6c
Create Date: 2024-04-06 18:27:32.007278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa9fed151ce1'
down_revision = '288edd42bc6c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('category', sa.Enum('FRIEND_REQUEST', 'FRIEND_ACCEPTED', 'BLOG_LIKE', 'BLOG_COMMENT', 'BLOG_SHARE', 'BLOG_PUBLISH', name='enumnotificationcategory'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_notifications_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    # ### end Alembic commands ###