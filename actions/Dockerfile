FROM rasa/rasa-sdk:3.6.1

WORKDIR /app

# Install curl for health checks (with proper permissions)
USER root
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5055

CMD ["start", "--actions", "actions"] 