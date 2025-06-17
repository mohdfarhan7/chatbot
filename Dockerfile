FROM rasa/rasa:3.6.16

# Copy all project files
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Train model at build time
RUN rasa train

# Expose the port
EXPOSE 5005

# Start Rasa server
CMD ["run", "--enable-api", "--cors", "*", "--debug"]