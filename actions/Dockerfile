FROM rasa/rasa-sdk:3.6.1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5055

CMD ["start", "--actions", "actions"] 