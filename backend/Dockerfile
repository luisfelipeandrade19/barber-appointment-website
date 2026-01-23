FROM python:3.13-slim

WORKDIR /app

# Install system dependencies required for psycopg2 and other potential builds
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy project configuration
COPY pyproject.toml poetry.lock ./

# Install dependencies (without creating a virtualenv inside the container, as we are isolated)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
