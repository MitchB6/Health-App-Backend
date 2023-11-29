"""empty message

Revision ID: b4b2e22123e5
Revises: 
Create Date: 2023-11-29 16:04:39.625649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4b2e22123e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('coaches_members_link', schema=None) as batch_op:
        batch_op.drop_constraint('coaches_members_link_ibfk_1', type_='foreignkey')
        batch_op.drop_constraint('coaches_members_link_ibfk_2', type_='foreignkey')
        batch_op.create_foreign_key(None, 'members', ['member_id'], ['member_id'], ondelete='CASCADE')
        batch_op.create_foreign_key(None, 'coach_info', ['coach_id'], ['coach_id'], ondelete='CASCADE')

    with op.batch_alter_table('personal_info', schema=None) as batch_op:
        batch_op.drop_constraint('personal_info_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'members', ['member_id'], ['member_id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('personal_info', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('personal_info_ibfk_1', 'members', ['member_id'], ['member_id'])

    with op.batch_alter_table('coaches_members_link', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('coaches_members_link_ibfk_2', 'members', ['member_id'], ['member_id'])
        batch_op.create_foreign_key('coaches_members_link_ibfk_1', 'coach_info', ['coach_id'], ['coach_id'])

    # ### end Alembic commands ###