from typing import Optional
import datetime
from collections import defaultdict
from flask_sqlalchemy.model import DefaultMeta
from flask_app.enums import CategoryTypes

from flask_app import db
from sqlalchemy import func
from flask_app.models import Spending


DATE_FORMAT = "%d-%m-%Y"
groupedForOneYear = dict[int, dict[str, list[tuple]]]


def date_validator(provided_date: str) -> Optional[str]:
    try:
        date_as_datetime = datetime.datetime.strptime(provided_date, DATE_FORMAT)
        formatted_date = date_as_datetime.strftime(DATE_FORMAT)
    except ValueError:
        return
    return formatted_date


def get_unique_queries_for_category_type(
    db_model: DefaultMeta, category_type: CategoryTypes
) -> list:
    query_to_return = (
        db_model.query.filter_by(category_type=category_type.value)
        .with_entities(db_model.category_name)
        .distinct()
        .all()
    )
    return query_to_return


def transform_grouped_query_to_dict_type_one_month(
    grouped_spending: list[tuple],
) -> dict[str, list[tuple]]:
    grouped_spending_for_template: dict[str, list[tuple]] = defaultdict(list)
    for s in grouped_spending:
        key, *values = s
        grouped_spending_for_template[key].append(values)
    return grouped_spending_for_template


def transform_grouped_query_to_dict_type_one_year(
    grouped_spending: list[tuple],
) -> groupedForOneYear:
    month_groups_helper: dict[int, list[list[str, str, float]]] = defaultdict(list)
    for s in grouped_spending:
        month, *details = s
        month_groups_helper[int(month)].append(details)
    year_groups = defaultdict(list)
    for month, details in month_groups_helper.items():
        year_groups[month].append(
            transform_grouped_query_to_dict_type_one_month(details)
        )
    return year_groups


def get_one_year_grouped_spending(db_model: DefaultMeta):
    grouped_spending = (
        db.session.query(
            func.extract("month", db_model.date),
            db_model.main_category,
            db_model.subcategory,
            func.sum(db_model.price),
        )
        .group_by(
            func.extract("month", db_model.date),
            db_model.main_category,
            db_model.subcategory,
        )
        .all()
    )
    return grouped_spending


def get_one_month_grouped_spending(db_model: DefaultMeta, year, month):
    grouped_spending = (
        db.session.query(
            db_model.main_category, db_model.subcategory, func.sum(db_model.price)
        )
        .group_by(db_model.main_category, db_model.subcategory)
        .filter(func.extract("year", db_model.date) == year)
        .filter(func.extract("month", db_model.date) == month)
        .all()
    )
    return grouped_spending
