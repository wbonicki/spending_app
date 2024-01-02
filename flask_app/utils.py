import functools
from typing import Optional
import datetime
from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
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


def get_main_category_total_sum(
    one_month_summary: dict[str, list[tuple]]
) -> dict[str, float]:
    main_category_summary = dict()
    for main_category, main_category_spending in one_month_summary.items():
        main_category_summary[main_category] = functools.reduce(
            lambda x, y: x + y[1], main_category_spending, 0
        )
    return main_category_summary


def get_main_category_total_summary_for_one_year(
    one_year_summary: groupedForOneYear,
) -> dict[int, dict[str, float]]:
    main_category_summary = dict()
    for month, one_month_summary in one_year_summary.items():
        main_category_summary[month] = get_main_category_total_sum(one_month_summary)
    return main_category_summary


def transform_grouped_query_to_dict_type_one_year(
    grouped_spending: list[tuple],
) -> groupedForOneYear:
    month_groups_helper: dict[int, list[list[str, str, float]]] = defaultdict(list)
    for s in grouped_spending:
        month, *details = s
        month_groups_helper[int(month)].append(details)
    year_groups = defaultdict(dict)
    for month, details in month_groups_helper.items():
        year_groups[month].update(
            transform_grouped_query_to_dict_type_one_month(details)
        )
    return year_groups


def get_one_year_grouped_spending(db: SQLAlchemy, db_model: DefaultMeta, year):
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
        .filter(func.extract("year", db_model.date) == year)
        .all()
    )
    return grouped_spending


def get_one_month_grouped_spending(db: SQLAlchemy, db_model: DefaultMeta, year, month):
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
