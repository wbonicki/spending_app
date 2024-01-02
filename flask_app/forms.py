from datetime import date
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    DateField,
    SubmitField,
    FloatField,
    SelectField,
    IntegerField
)
from wtforms.validators import ValidationError, DataRequired, NumberRange
from flask_app.enums import CategoryTypes
from flask_app.models import Category, Spending
from flask_app.utils import get_unique_queries_for_category_type
from sqlalchemy import func


ANALYZE_ONE_YEAR = "analyze_all_months"


class SpendingFormBase(FlaskForm):
    main_category = SelectField(validators=[DataRequired()])
    subcategory = SelectField(validators=[DataRequired()])
    price = FloatField("Price", validators=[DataRequired(), NumberRange(min=0.5)])
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d", default=date.today)
    def __init__(self):
        super(SpendingFormBase, self).__init__()
        db_model = Category
        categories = get_unique_queries_for_category_type(db_model, CategoryTypes.MAIN_CATEGORY)
        subcategories = get_unique_queries_for_category_type(db_model, CategoryTypes.SUBCATEGORY)
        self.main_category.choices = [(c[0], c[0]) for c in categories]
        self.subcategory.choices = [(s[0], s[0]) for s in subcategories]

class SpendingForm(SpendingFormBase):
    submit = SubmitField("Add Spending")

class EditSpendingForm(SpendingFormBase):
    submit = SubmitField("Edit Spending")

class GroupSpendingsForm(FlaskForm):
    year = SelectField(validators=[DataRequired()])
    month = SelectField(validators=[DataRequired()])
    submit = SubmitField("Generate analysis")

    def __init__(self):
        super(GroupSpendingsForm, self).__init__()
        unique_years = Spending.query.with_entities(func.extract("year", Spending.date)).distinct().all()
        unique_months = Spending.query.with_entities(func.extract("month", Spending.date)).distinct().all()
        self.year.choices = [(i[0], i[0]) for i in unique_years]
        self.month.choices = [(i[0], i[0]) for i in unique_months] + [(ANALYZE_ONE_YEAR, ANALYZE_ONE_YEAR)]


class NewCategoryForm(FlaskForm):
    category_type = SelectField(
        "Category type",
        choices=[(c.value, c.value) for c in CategoryTypes],
        validators=[DataRequired()],
    )
    category_name = StringField("Enter new category", validators=[DataRequired()])
    submit = SubmitField("Add new category")

    def validate_category_name(self, category_name):
        category = Category.query.filter_by(category_name=category_name.data).first()
        if category is not None:
            raise ValidationError("Category already exists.")


class RemoveCategoryForm(FlaskForm):
    category_name = StringField("Select category to remove", validators=[DataRequired()])
    submit = SubmitField("Remove category")

    def __init__(self):
        super(RemoveCategoryForm, self).__init__()
        db_model = Category
        categories = get_unique_queries_for_category_type(db_model, CategoryTypes.MAIN_CATEGORY)
        subcategories = get_unique_queries_for_category_type(db_model, CategoryTypes.SUBCATEGORY)
        all_categories = categories + subcategories
        self.category_name.choices = [(c[0], c[0]) for c in all_categories]
