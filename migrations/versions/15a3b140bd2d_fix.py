"""fix

Revision ID: 15a3b140bd2d
Revises: 6aae6b4acc46
Create Date: 2023-07-03 21:32:19.611033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '15a3b140bd2d'
down_revision = '6aae6b4acc46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.drop_constraint('categories_category_type_key', type_='unique')
        batch_op.drop_constraint('categories_category_type_key1', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        batch_op.create_unique_constraint('categories_category_type_key1', ['category_type'])
        batch_op.create_unique_constraint('categories_category_type_key', ['category_type'])

    # ### end Alembic commands ###
