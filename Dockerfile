# Start from a small, supported Python image
FROM python:3.11-slim

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install uv
# RUN uv venv docker && source docker/bin/activate
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Default port for Fly is provided via $PORT; fall back to 8080
ENV PORT=8080

# Expose the fallback port (informational)
EXPOSE 8080

# Use sh -c so we can expand $PORT at runtime
ENTRYPOINT ["sh", "-c", "uvicorn fast_api_server:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers"]
