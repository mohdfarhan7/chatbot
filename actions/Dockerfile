FROM python:3.8-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements-actions.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-actions.txt

# Copy the rest of the application
COPY . .

# Start the action server
CMD ["rasa", "run", "actions"] 