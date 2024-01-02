from decimal import Decimal
from flask_testing import TestCase
from datetime import datetime
from tests import app, db
from tests.models import Spending, Category
from flask_app.enums import CategoryTypes
from flask_app.utils import (
    get_one_month_grouped_spending,
    get_one_year_grouped_spending,
    get_unique_queries_for_category_type
)


class TestDb(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        pass
        # db.create_all()

    def tearDown(self):
        Spending.query.delete()
        Category.query.delete()
        db.session.commit()

    def test_get_one_month_grouped_spending(self):
        spending = Spending(
            main_category="food",
            subcategory="meat",
            price=100.0,
            date=datetime(2000, 1, 1),
        )
        db.session.add(spending)
        spending = Spending(
            main_category="food",
            subcategory="meat",
            price=200.0,
            date=datetime(2000, 1, 20),
        )
        db.session.add(spending)

        spending = Spending(
            main_category="car",
            subcategory="petrol",
            price=250.0,
            date=datetime(2000, 1, 10),
        )
        db.session.add(spending)
        db.session.commit()
        result = get_one_month_grouped_spending(db, Spending, 2000, 1)

        correct_result = {("car", "petrol", 250.0), ("food", "meat", 300.0)}
        self.assertEqual(set(result), correct_result)

    def test_get_one_year_grouped_spending(self):
        spending = Spending(
            main_category="food",
            subcategory="meat",
            price=100.0,
            date=datetime(2000, 1, 1),
        )
        db.session.add(spending)
        spending = Spending(
            main_category="food",
            subcategory="meat",
            price=200.0,
            date=datetime(2000, 1, 20),
        )
        db.session.add(spending)

        spending = Spending(
            main_category="food",
            subcategory="meat",
            price=200.0,
            date=datetime(2000, 2, 20),
        )
        db.session.add(spending)
        spending = Spending(
            main_category="car",
            subcategory="petrol",
            price=250.0,
            date=datetime(2000, 2, 10),
        )
        db.session.add(spending)
        db.session.commit()
        result = get_one_year_grouped_spending(db, Spending, 2000)
        correct_result = {
            (Decimal("1"), "food", "meat", 300.0),
            (Decimal("2"), "car", "petrol", 250.0),
            (Decimal("2"), "food", "meat", 200.0),
        }
        self.assertEqual(set(result), correct_result)

    def test_get_unique_queries_for_category_type(self):

        category = Category(category_type=CategoryTypes.MAIN_CATEGORY.value, category_name="car")
        db.session.add(category)
        category = Category(category_type=CategoryTypes.MAIN_CATEGORY.value, category_name="food")
        db.session.add(category)
        db.session.commit()

        result = get_unique_queries_for_category_type(Category, CategoryTypes.MAIN_CATEGORY)
        correct_result = {('car',), ('food',)}
        self.assertEqual(set(result), correct_result)
