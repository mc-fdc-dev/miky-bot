FROM python:3-slim AS package

WORKDIR /app/package

RUN pip install poetry
COPY pyproject.toml poetry.lock .

RUN poetry export -f requirements.txt -o requirements.txt

FROM python:3-slim

WORKDIR /app/bot

COPY --from=package /app/package/requirements.txt .
RUN pip install -r requirements.txt

COPY ./src .

CMD ["python3", "main.py"]
