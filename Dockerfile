# Use python 3.10 slim image
FROM python:3.10-slim

# Install system dependencies
# ffmpeg: required for audio processing
# git: required for uv to install git dependencies if any
# curl: required to install uv
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv (modern python package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy dependency files first
COPY pyproject.toml uv.lock* ./

# Install dependencies
# --no-dev: optimized for production
# --no-install-project: we install the project files later
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the application
COPY . .

# Install the project itself
RUN uv sync --frozen --no-dev

# Expose the application port
EXPOSE 12393

# Run the server
CMD ["uv", "run", "run_server.py"]
