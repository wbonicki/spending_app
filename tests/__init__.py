from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class TestsConfig:
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://test:test@0.0.0.0:5444/test"
   
app = Flask(__name__)
app.config.from_object(TestsConfig)
db = SQLAlchemy(app)
