# ========= BASE =========
FROM python:3.11-slim AS base
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ========= DEVELOPMENT =========
FROM base AS development
# Copy source
COPY ./app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


# ========= PRODUCTION =========
FROM base AS production
RUN adduser --disabled-password --gecos '' appuser
USER appuser
# Copy source
COPY ./app ./app
# Gunakan workers uvicorn untuk performa
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
