FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install requirements first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir "uvicorn[standard]"

# Copy app & model
COPY app ./app
COPY models ./models

# Security: non-root user
RUN useradd -m appuser
USER appuser

EXPOSE 8080
ENV MODEL_PATH=models/heart.joblib
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
