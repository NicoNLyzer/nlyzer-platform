# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY nlyzer/ ./nlyzer/

# Expose port 8000
EXPOSE 8000

# Default command to run the application
CMD ["uvicorn", "nlyzer.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]