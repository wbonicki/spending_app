FROM python:3.11.3-slim AS base

WORKDIR /spending_app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY flask_app flask_app
COPY tests tests
RUN rm tests/test_db.py
COPY main.py .
COPY docker-compose/.env .
EXPOSE 5000

RUN python -m unittest discover tests
ENTRYPOINT ["python", "main.py"]