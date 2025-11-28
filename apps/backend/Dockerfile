# Use official slim Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and tests
COPY app ./app
COPY tests ./tests

# Set PYTHONPATH for app imports
ENV PYTHONPATH=/app

# Expose backend port
EXPOSE 8000

# Set default run mode
ENV RUN_MODE=run

CMD ["sh", "-c", "\
if [ \"$RUN_MODE\" = \"test\" ]; then \
    echo 'Running unit tests...' && python -m unittest discover -s tests -v; \
else \
    echo 'Starting app...' && uvicorn app.main:app --host 0.0.0.0 --port 8000; \
fi \
"]
