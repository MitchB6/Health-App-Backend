"""empty message

Revision ID: dec7539844da
Revises: 
Create Date: 2023-11-29 12:26:55.133353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'dec7539844da'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=100), nullable=True))
        batch_op.drop_column('username')

    with op.batch_alter_table('personal_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=255), nullable=True))
        batch_op.drop_index('email')
        batch_op.create_unique_constraint(None, ['username'])
        batch_op.drop_column('email')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('personal_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', mysql.VARCHAR(length=255), nullable=True))
        batch_op.drop_constraint(None, type_='unique')
        batch_op.create_index('email', ['email'], unique=False)
        batch_op.drop_column('username')

    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', mysql.VARCHAR(length=100), nullable=True))
        batch_op.drop_column('email')

    # ### end Alembic commands ###