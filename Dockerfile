FROM python:3.10-slim

WORKDIR /app

COPY ./ /app

RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
