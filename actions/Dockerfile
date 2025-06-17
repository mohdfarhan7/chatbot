FROM python:3.7-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    python3-venv \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy actions code
COPY . /app/actions

# Install additional dependencies
RUN pip install --no-cache-dir -r /app/actions/requirements.txt

# Expose the port
EXPOSE 5055

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=5055

# Start the action server
CMD ["rasa", "run", "actions"] 