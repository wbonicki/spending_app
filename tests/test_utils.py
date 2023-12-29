import os
import unittest
from flask_app.utils import transform_grouped_query_to_dict_type_one_month


class TestAppUtils(unittest.TestCase):
    def test_transform_grouped_query_to_dict_type_one_month(self):

        grouped_spending = [
            ("car", "petrol", 100.0),
            ("car", "tires", 250.0),
            ("food", "meat", 100.0),
            ("food", "fruits", 150.0),
        ]

        grouped_spending_for_month = transform_grouped_query_to_dict_type_one_month(grouped_spending)
        correct_result = {"car": [["petrol", 100.0], ["tires", 250.0]], "food": [["meat", 100.0], ["fruits", 150.0]]}

        self.assertEqual(grouped_spending_for_month, correct_result)
