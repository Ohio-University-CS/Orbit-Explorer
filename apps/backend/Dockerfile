FROM python:3.13-slim

WORKDIR /app

COPY app ./app
COPY tests ./tests
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8000

ENV RUN_MODE=run

CMD if [ "$RUN_MODE" = "test" ]; then \
      echo "Running unit tests..." && python -m unittest discover -s tests -v; \
    else \
      echo "Starting app..." && uvicorn app.main:app --host 0.0.0.0 --port 8000; \
    fi