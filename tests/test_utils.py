import unittest
from decimal import Decimal
from flask_app.utils import (
    transform_grouped_query_to_dict_type_one_month,
    transform_grouped_query_to_dict_type_one_year,
    get_main_category_total_sum,
    get_main_category_total_summary_for_one_year,
)


class TestAppUtils(unittest.TestCase):
    def test_transform_grouped_query_to_dict_type_one_month(self):
        grouped_spending = [
            ("car", "petrol", 100.0),
            ("car", "tires", 250.0),
            ("food", "meat", 100.0),
            ("food", "fruits", 150.0),
        ]

        grouped_spending_for_month = transform_grouped_query_to_dict_type_one_month(
            grouped_spending
        )
        correct_result = {
            "car": [["petrol", 100.0], ["tires", 250.0]],
            "food": [["meat", 100.0], ["fruits", 150.0]],
        }

        self.assertEqual(grouped_spending_for_month, correct_result)

    def test_transform_grouped_query_to_dict_type_one_year(self):
        one_year_spending = [
            (Decimal("10"), "food", "bread", 55.0),
            (Decimal("10"), "food", "fruits", 35.0),
            (Decimal("11"), "car", "petrol", 100.0),
            (Decimal("11"), "food", "fruits", 120.0),
            (Decimal("12"), "car", "oil", 200.0),
            (Decimal("12"), "food", "bread", 50.0),
            (Decimal("12"), "food", "fruits", 20.0),
        ]
        grouped_spending_for_month = transform_grouped_query_to_dict_type_one_year(
            one_year_spending
        )
        correct_result = {
            10: {"food": [["bread", 55.0], ["fruits", 35.0]]},
            11: {"car": [["petrol", 100.0]], "food": [["fruits", 120.0]]},
            12: {"car": [["oil", 200.0]], "food": [["bread", 50.0], ["fruits", 20.0]]},
        }

        self.assertEqual(grouped_spending_for_month, correct_result)

    def test_get_main_category_total_sum(self):
        input_data = {
            "car": [["petrol", 100.0], ["tires", 250.0]],
            "food": [["meat", 100.0], ["fruits", 150.0]],
            "sport": [["shoes", 300.0], ["gym", 250.0]],
        }
        result = get_main_category_total_sum(input_data)
        correct_result = {"car": 350.0, "food": 250.0, "sport": 550.0}
        self.assertEqual(result, correct_result)

    def test_get_main_category_total_summary_for_one_year(self):
        input_data = {
            10: {
                "food": [["bread", 55.0], ["fruits", 35.0]],
                "car": [["petrol", 100.0], ["tires", 250.0]],
            },
            11: {"car": [["petrol", 100.0]], "food": [["fruits", 120.0]]},
            12: {"car": [["oil", 200.0]], "food": [["bread", 50.0], ["fruits", 20.0]]},
        }

        result = get_main_category_total_summary_for_one_year(input_data)
        correct_result = {10: {'food': 90.0, 'car': 350.0}, 11: {'car': 100.0, 'food': 120.0}, 12: {'car': 200.0, 'food': 70.0}}
        self.assertEqual(result, correct_result)

        one_year_months_total = {month: sum(main_category_spending.values()) for month, main_category_spending in result.items()}
        correct_result = {10: 440.0, 11: 220.0, 12: 270.0}
        self.assertEqual(one_year_months_total, correct_result)
