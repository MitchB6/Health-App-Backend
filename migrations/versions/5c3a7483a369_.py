"""empty message

Revision ID: 5c3a7483a369
Revises: 
Create Date: 2023-12-04 18:29:40.806736

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c3a7483a369'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercises', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercises', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
