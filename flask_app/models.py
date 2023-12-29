from flask_app import db


class Spending(db.Model):
    __tablename__ = "spendings"
    id = db.Column(db.Integer, primary_key=True)
    main_category = db.Column(db.String, nullable=False)
    subcategory = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, db.CheckConstraint("price > 0"))
    date = db.Column(db.Date, nullable=False)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    category_type = db.Column(db.String, nullable=False)
    category_name = db.Column(db.String, nullable=False, unique=True)
