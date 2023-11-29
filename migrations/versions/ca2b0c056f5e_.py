"""empty message

Revision ID: ca2b0c056f5e
Revises: 6cc079c4da96
Create Date: 2023-11-29 16:22:52.186415

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca2b0c056f5e'
down_revision = '6cc079c4da96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('availability', schema=None) as batch_op:
        batch_op.drop_constraint('availability_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'coach_info', ['coach_id'], ['coach_id'], ondelete='CASCADE')

    with op.batch_alter_table('exercise_stats', schema=None) as batch_op:
        batch_op.drop_constraint('exercise_stats_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'exercises', ['exercise_id'], ['exercise_id'], ondelete='CASCADE')

    with op.batch_alter_table('workout_exercises', schema=None) as batch_op:
        batch_op.drop_constraint('workout_exercises_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'workouts', ['workout_id'], ['workout_id'], ondelete='CASCADE')

    with op.batch_alter_table('workout_plan_links', schema=None) as batch_op:
        batch_op.drop_constraint('workout_plan_links_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'workout_plans', ['plan_id'], ['plan_id'], ondelete='CASCADE')

    with op.batch_alter_table('workout_plans', schema=None) as batch_op:
        batch_op.drop_constraint('workout_plans_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'members', ['member_id'], ['member_id'], ondelete='CASCADE')

    with op.batch_alter_table('workout_stats', schema=None) as batch_op:
        batch_op.drop_constraint('workout_stats_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'workouts', ['workout_id'], ['workout_id'], ondelete='CASCADE')

    with op.batch_alter_table('workouts', schema=None) as batch_op:
        batch_op.drop_constraint('workouts_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'members', ['member_id'], ['member_id'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('workouts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('workouts_ibfk_1', 'members', ['member_id'], ['member_id'])

    with op.batch_alter_table('workout_stats', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('workout_stats_ibfk_1', 'workouts', ['workout_id'], ['workout_id'])

    with op.batch_alter_table('workout_plans', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('workout_plans_ibfk_1', 'members', ['member_id'], ['member_id'])

    with op.batch_alter_table('workout_plan_links', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('workout_plan_links_ibfk_1', 'workout_plans', ['plan_id'], ['plan_id'])

    with op.batch_alter_table('workout_exercises', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('workout_exercises_ibfk_1', 'workouts', ['workout_id'], ['workout_id'])

    with op.batch_alter_table('exercise_stats', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('exercise_stats_ibfk_1', 'exercises', ['exercise_id'], ['exercise_id'])

    with op.batch_alter_table('availability', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('availability_ibfk_1', 'coach_info', ['coach_id'], ['coach_id'])

    # ### end Alembic commands ###