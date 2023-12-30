import os
from dotenv import load_dotenv

dotenv_file_path = os.path.join(os.path.dirname(__file__), "../", ".env")
docker_environment = os.path.isfile(dotenv_file_path) is True
if docker_environment is False:
    dotenv_file_path = (os.path.join(os.path.dirname(__file__), '../docker-compose', '.env'))

load_dotenv(dotenv_file_path)


class Config:
    user = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")
    service_name = os.environ.get("SERVICE_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{user}:{password}@{service_name}:{db_port}/{db_name}"
    )
    SECRET_KEY = "very_secret_key"
