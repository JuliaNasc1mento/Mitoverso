"""forum: posts, curtidas, seguidores e perfil

Revision ID: a1c3f9d2b7e4
Revises: 7534d6449b8d
Create Date: 2026-10-28 20:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1c3f9d2b7e4'
down_revision = '7534d6449b8d'
branch_labels = None
depends_on = None


def upgrade():
    # Novos campos do perfil (nullable para não quebrar usuários já cadastrados)
    op.add_column('usuario', sa.Column('bio', sa.String(length=200), nullable=True))
    op.add_column('usuario', sa.Column('criado_em', sa.DateTime(), nullable=True))

    op.create_table('seguidor',
    sa.Column('id_seguidor', sa.Integer(), nullable=False),
    sa.Column('id_seguido', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_seguido'], ['usuario.id'], ),
    sa.ForeignKeyConstraint(['id_seguidor'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id_seguidor', 'id_seguido')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conteudo', sa.Text(), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('id_pai', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_pai'], ['post.id'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('curtida',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_usuario', sa.Integer(), nullable=False),
    sa.Column('id_post', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_post'], ['post.id'], ),
    sa.ForeignKeyConstraint(['id_usuario'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_usuario', 'id_post', name='uq_curtida_usuario_post')
    )


def downgrade():
    op.drop_table('curtida')
    op.drop_table('post')
    op.drop_table('seguidor')
    with op.batch_alter_table('usuario') as batch_op:
        batch_op.drop_column('criado_em')
        batch_op.drop_column('bio')
