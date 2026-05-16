"""add user test results

Revision ID: 003_add_test_results
Revises: 099a0c4fabc6
Create Date: 2026-05-16

"""
from alembic import op
import sqlalchemy as sa

revision = '003_add_test_results'
down_revision = '099a0c4fabc6'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('user_test_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('test_id', sa.Integer(), nullable=False),
        sa.Column('answer', sa.String(), nullable=False),
        sa.Column('is_correct', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['test_id'], ['tests.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_test_results_id'), 'user_test_results', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_user_test_results_id'), table_name='user_test_results')
    op.drop_table('user_test_results')