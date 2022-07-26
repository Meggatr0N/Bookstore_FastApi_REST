"""First revision

Revision ID: d793556bf26b
Revises: 
Create Date: 2022-08-17 11:57:51.720097

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "d793556bf26b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("order_items")
    op.drop_index("ix_books_id", table_name="books")
    op.drop_table("books")
    op.drop_index("ix_categories_id", table_name="categories")
    op.drop_table("categories")
    op.drop_index("ix_authors_id", table_name="authors")
    op.drop_table("authors")
    op.drop_index("ix_orders_id", table_name="orders")
    op.drop_table("orders")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('users_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "fullname", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "password", sa.VARCHAR(), autoincrement=False, nullable=True
        ),
        sa.Column("role", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        sa.UniqueConstraint("email", name="users_email_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_users_id", "users", ["id"], unique=False)
    op.create_table(
        "orders",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('orders_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "date_placed",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "customer_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "total_price",
            sa.NUMERIC(precision=10, scale=2),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("paid", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            "delivery_date", sa.DATE(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "complete", sa.BOOLEAN(), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["customer_id"], ["users.id"], name="orders_customer_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="orders_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_orders_id", "orders", ["id"], unique=False)
    op.create_table(
        "authors",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('authors_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name", sa.VARCHAR(length=64), autoincrement=False, nullable=False
        ),
        sa.Column(
            "email", sa.VARCHAR(length=64), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="authors_pkey"),
        sa.UniqueConstraint("name", name="authors_name_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_authors_id", "authors", ["id"], unique=False)
    op.create_table(
        "categories",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('categories_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name", sa.VARCHAR(length=64), autoincrement=False, nullable=False
        ),
        sa.Column(
            "is_active", sa.BOOLEAN(), autoincrement=False, nullable=True
        ),
        sa.PrimaryKeyConstraint("id", name="categories_pkey"),
        sa.UniqueConstraint("name", name="categories_name_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_categories_id", "categories", ["id"], unique=False)
    op.create_table(
        "books",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('books_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name", sa.VARCHAR(length=128), autoincrement=False, nullable=False
        ),
        sa.Column(
            "price",
            sa.NUMERIC(precision=10, scale=2),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "description", sa.TEXT(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "year_of_publication",
            sa.INTEGER(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "is_active", sa.BOOLEAN(), autoincrement=False, nullable=True
        ),
        sa.Column(
            "author_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "category_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["author_id"], ["authors.id"], name="books_author_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["category_id"], ["categories.id"], name="books_category_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="books_pkey"),
        sa.UniqueConstraint("name", name="books_name_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_index("ix_books_id", "books", ["id"], unique=False)
    op.create_table(
        "order_items",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "order_id", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column("book_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "quantity", sa.SMALLINT(), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["book_id"], ["books.id"], name="order_items_book_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["order_id"], ["orders.id"], name="order_items_order_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="order_items_pkey"),
    )
    # ### end Alembic commands ###
