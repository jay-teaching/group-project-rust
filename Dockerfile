# Pick a base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv as per official docs
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy uv project configuration
COPY pyproject.toml .
COPY uv.lock .

# Copy project files
COPY notebooks/ notebooks/
COPY models/ models/
COPY input/ input/
COPY prediction.py .
COPY .python-version .

# Install dependencies with uv
RUN uv sync

# Expose port for marimo
EXPOSE 8080

# Run marimo with uv
CMD ["uv", "run", "marimo", "run", "notebooks/telco_predictor.py", "--host", "0.0.0.0", "--port", "8080"]
