from flask import render_template, flash, url_for, redirect, request
from sqlalchemy import func
from flask_app import app, db
from flask_app.forms import (
    SpendingForm,
    NewCategoryForm,
    RemoveCategoryForm,
    GroupSpendingsForm,
    EditSpendingForm,
    ANALYZE_ONE_YEAR,
)
from flask_app.models import Spending, Category
from flask_app.utils import (
    transform_grouped_query_to_dict_type_one_month,
    transform_grouped_query_to_dict_type_one_year,
    get_main_category_total_summary_for_one_year,
    get_one_year_grouped_spending,
    get_one_month_grouped_spending,
    get_main_category_total_sum,
)


@app.route("/main")
@app.route("/")
def main():
    return render_template("main.html")


@app.route("/add", methods=["POST", "GET"])
def spending_adder():
    form = SpendingForm()
    if form.validate_on_submit():
        category, subcategory, price, spending_date = (
            form.main_category.data,
            form.subcategory.data,
            form.price.data,
            form.date.data,
        )
        message_to_display = (
            "Your spending has been added!\n"
            f"Main category: {category}, subcategory: {subcategory}, price: {price}"
        )
        spending = Spending(
            main_category=category,
            subcategory=subcategory,
            price=price,
            date=spending_date,
        )
        db.session.add(spending)
        db.session.commit()
        flash(message_to_display)
        return redirect(url_for("spending_adder"))
    return render_template("add.html", form=form)


@app.route("/analyze", methods=["POST", "GET"])
def spending_analyzer():
    all_spendings = Spending.query.order_by(Spending.date.desc()).all()
    form = GroupSpendingsForm()
    if form.validate_on_submit():
        year, month = form.year.data, form.month.data
        if month == ANALYZE_ONE_YEAR:
            grouped_spending = get_one_year_grouped_spending(db, Spending, year)
            grouped_spending_for_template = (
                transform_grouped_query_to_dict_type_one_year(grouped_spending)
            )
            one_year_main_categores_spending_sum = (
                get_main_category_total_summary_for_one_year(
                    grouped_spending_for_template
                )
            )
            one_year_months_total = {
                month: sum(main_category_spending.values())
                for month, main_category_spending in one_year_main_categores_spending_sum.items()
            }
            return render_template(
                "year_analyzer.html",
                year=year,
                grouped_spendings_year=grouped_spending_for_template,
                one_year_main_categores_spending_sum=one_year_main_categores_spending_sum,
                one_year_months_total=one_year_months_total
            )
        else:
            spending_exists = Spending.query.where(
                func.extract("year", Spending.date) == year,
                func.extract("month", Spending.date) == month,
            ).all()
            if spending_exists is None:
                flash("In selected month were no spendings!")
            grouped_spending = get_one_month_grouped_spending(db, Spending, year, month)
            grouped_spending_for_template = (
                transform_grouped_query_to_dict_type_one_month(grouped_spending)
            )
            one_month_main_categores_spending_sum = get_main_category_total_sum(
                grouped_spending_for_template
            )
            one_month_total_sum = sum(one_month_main_categores_spending_sum.values())
            return render_template(
                "month_analyzer.html",
                year=year,
                month=month,
                grouped_spendings=grouped_spending_for_template,
                one_month_main_categores_spending_sum=one_month_main_categores_spending_sum,
                one_month_total_sum=one_month_total_sum,
            )
    return render_template("analyzer.html", all_spendings=all_spendings, form=form)


@app.route("/remove_spending", methods=["POST", "GET"])
def remove_spending():
    if request.method == "POST":
        spending = Spending.query.filter_by(id=request.form["Spending_ID"]).first()
        if spending is None:
            flash("No such ID!")
            return redirect(url_for("remove_spending"))
        db.session.delete(spending)
        db.session.commit()
        return redirect(url_for("spending_analyzer"))
    return render_template("remove_spending.html")


@app.route("/edit_spending", methods=["POST", "GET"])
def edit_spending():
    if request.method == "POST":
        spending_id = request.form["Spending_ID"]
        return redirect(url_for("edit_spending_with_id", spending_id=spending_id))
    return render_template("get_spending_by_id.html")


@app.route("/edit_spending_with_id", methods=["POST", "GET"])
def edit_spending_with_id():
    spending_id = request.args.get("spending_id")
    spending = Spending.query.filter_by(id=spending_id).first()
    if spending is None:
        flash("No such ID!")
        return redirect(url_for("edit_spending"))
    old_values = spending.to_dict()
    form = EditSpendingForm()
    if form.validate_on_submit():
        category, subcategory, price, date = (
            form.main_category.data,
            form.subcategory.data,
            form.price.data,
            form.date.data,
        )
        spending.main_category = (category,)
        spending.subcategory = (subcategory,)
        spending.price = (price,)
        spending.date = date
        db.session.commit()
        message_to_display = f"Spending with ID={spending.id} has been edited!\n"
        flash(message_to_display)
        return redirect(url_for("spending_analyzer"))
    return render_template("edit_spending.html", form=form, old_values=old_values)


@app.route("/add_new_category", methods=["POST", "GET"])
def add_new_category():
    form = NewCategoryForm()
    if form.validate_on_submit():
        category_type, category_name = form.category_type.data, form.category_name.data
        new_category = Category(
            category_type=category_type, category_name=category_name
        )
        db.session.add(new_category)
        db.session.commit()
        flash("New category added!")
    return render_template("add_new_category.html", form=form)


@app.route("/remove_existing_category", methods=["POST", "GET"])
def remove_category():
    form = RemoveCategoryForm()
    if form.validate_on_submit():
        category_name = form.category_name.data
        category_to_remove = Category.query.filter_by(
            category_name=category_name
        ).first()
        db.session.delete(category_to_remove)
        db.session.commit()
        flash(f"Category {category_name} removed!")
        return redirect(url_for("spending_adder"))
    return render_template("remove_category.html", form=form)
