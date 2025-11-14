FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create upload directory
RUN mkdir -p static/uploads

# Expose ports
EXPOSE 5000 5001 5002

# Default command (can be overridden in docker-compose)
CMD ["gunicorn", "adoption_system.app:app", "--bind", "0.0.0.0:5000", "--workers", "2"]
