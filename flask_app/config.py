import os
from dotenv import load_dotenv

dotenv_file_path = (os.path.join(os.path.dirname(__file__), '../docker-compose', '.env'))
load_dotenv(dotenv_file_path)


class Config:
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")
    service_name = os.environ.get("SERVICE_NAME")
    # SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://postgres:password@172.17.0.2:5432/spending_app"
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{user}:{password}@{service_name}:{db_port}/{db_name}"
    print(SQLALCHEMY_DATABASE_URI)
    SECRET_KEY = "very_secret_key"
