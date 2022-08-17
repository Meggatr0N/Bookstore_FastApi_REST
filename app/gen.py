from faker import Faker
import random

from app.models import user_m, order_m, store_m
from app.schemas import user_order_s
from app.crud import order_logic
from app.database.db import SessionLocal
from app.core import security

session = SessionLocal()
faker = Faker()

number_of_authors = 20
number_of_categories = 20
number_of_books = 1000
number_of_users = 100
number_of_orders = 300


def data_generator():

    # create authors
    for i in range(1, number_of_authors):
        author = store_m.Author(
            name=faker.name() + str(i),
            email=faker.email(),
        )
        session.add(author)

    # create categories
    for i in range(1, number_of_authors):
        category = store_m.Category(
            name=faker.street_suffix() + str(i),
            is_active=True,
        )
        session.add(category)
    session.commit()

    # create books
    for i in range(1, number_of_books):
        book = store_m.Book(
            name=f"Book {i}",
            price=round(random.uniform(2.5, 7.25), 2),
            description=faker.text(),
            year_of_publication=faker.year(),
            is_active=True,
            author_id=random.randint(1, number_of_authors - 1),
            category_id=random.randint(1, number_of_categories - 1),
        )
        session.add(book)

    session.commit()

    # create admin user
    user = user_m.User(
        fullname="Admin Artem",
        email="artem@gmail.com",
        password=security.get_hashed_password("artemartem"),
        role="admin",
    )
    session.add(user)

    # create users
    for i in range(1, number_of_users):
        user = user_m.User(
            fullname=faker.name(),
            email=faker.email(),
            password=security.get_hashed_password(faker.password()),
        )
        session.add(user)

    session.commit()

    # create user's orders
    for i in range(1, number_of_orders):
        order_item_data = []
        for _ in range(random.randint(1, 3)):
            order_item_data.append(
                {
                    "book_id": random.randint(1, number_of_books - 1),
                    "quantity": random.randint(1, 4),
                }
            )

        order_item = [
            user_order_s.OrderItemCreate(**item_data)
            for item_data in order_item_data
        ]
        random_user_id = random.randint(1, number_of_users - 1)
        user = (
            session.query(user_m.User)
            .filter(user_m.User.id == int(random_user_id))
            .first()
        )

        item: order_m.Order = order_logic.create_item(
            item=order_item,
            db=session,
            current_user=user,
        )
        session.add(item)
    session.commit()
