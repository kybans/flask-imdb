"""empty message

Revision ID: e90032f55996
Revises: 
Create Date: 2018-06-01 03:07:33.854074

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e90032f55996'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre_name', sa.String(length=10), nullable=True),
    sa.Column('update_dttm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.Column('create_dttm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_name', sa.String(length=12), nullable=True),
    sa.Column('director_name', sa.String(length=12), nullable=True),
    sa.Column('imdb_score', sa.Float(), nullable=True),
    sa.Column('99popularity', sa.Float(), nullable=True),
    sa.Column('update_dttm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.Column('create_dttm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('movie_genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('update_dttm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.Column('create_dttm', sa.DateTime(timezone=True), server_default=sa.text(u'now()'), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=True),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('movie_genre')
    op.drop_table('movie')
    op.drop_table('genre')
    # ### end Alembic commands ###
