FROM python:3.11.3-slim AS base

WORKDIR /spending_app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY flask_app flask_app
COPY tests tests
COPY main.py .
COPY docker-compose/.env .
EXPOSE 5000

RUN python -m unittest -v tests
ENTRYPOINT ["python", "main.py"]