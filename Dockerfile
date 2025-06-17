FROM rasa/rasa:3.6.21

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Train the model
RUN rasa train

EXPOSE 5005

CMD ["run", "--enable-api", "--cors", "*"]