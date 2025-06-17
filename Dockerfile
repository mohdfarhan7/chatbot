FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Train Rasa model
RUN rasa train

# Expose the port
EXPOSE 10000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Start the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "10000"]