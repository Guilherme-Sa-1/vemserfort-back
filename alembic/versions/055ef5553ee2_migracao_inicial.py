"""Migracao Inicial

Revision ID: 055ef5553ee2
Revises: 
Create Date: 2025-07-09 16:28:47.819735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '055ef5553ee2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cursos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('professor', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('senha', sa.String(), nullable=False),
    sa.Column('ativo', sa.Boolean(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('aulas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('curso_id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(), nullable=False),
    sa.Column('data_aula', sa.DateTime(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.Column('link_forms_frequencia', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['curso_id'], ['cursos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matriculas',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('curso_id', sa.Integer(), nullable=False),
    sa.Column('data_matricula', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['curso_id'], ['cursos.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('frequencias',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('aula_id', sa.Integer(), nullable=False),
    sa.Column('data_registro', sa.DateTime(), nullable=True),
    sa.Column('presente', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['aula_id'], ['aulas.id'], ),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('frequencias')
    op.drop_table('matriculas')
    op.drop_table('aulas')
    op.drop_table('usuarios')
    op.drop_table('cursos')
    # ### end Alembic commands ###
