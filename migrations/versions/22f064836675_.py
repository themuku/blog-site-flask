"""empty message

Revision ID: 22f064836675
Revises: 
Create Date: 2024-03-29 14:36:04.986299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22f064836675'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('role', sa.Enum('admin', 'user'), nullable=True),
    sa.Column('profile_img', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('author_name', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subtitle', sa.String(length=255), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('blog_img', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_blogs_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blogs')
    op.drop_table('users')
    # ### end Alembic commands ###