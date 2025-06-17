FROM rasa/rasa:3.6.1

WORKDIR /app

# Switch to root user and install curl
USER root
RUN rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Train the model
RUN rasa train

EXPOSE 5005

CMD ["run", "--enable-api", "--cors", "*"]