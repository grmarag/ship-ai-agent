# Use the official slim Python image.
FROM python:3.12-slim

# Set environment variables to ensure output is immediately flushed.
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (adjust POETRY_VERSION as needed)
ENV POETRY_VERSION=1.5.1
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure that Poetry's bin directory is in PATH.
ENV PATH="/root/.local/bin:${PATH}"

# Set the working directory in the container.
WORKDIR /app

# Copy only the dependency descriptor files first (to leverage Docker caching)
COPY pyproject.toml poetry.lock* ./

# Configure Poetry to install dependencies into the container’s system environment
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application code.
COPY . .

# Expose the port that Streamlit uses (8501 by default)
EXPOSE 8501

# Set environment variables for Streamlit.
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501

# Run the Streamlit app.
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false"]