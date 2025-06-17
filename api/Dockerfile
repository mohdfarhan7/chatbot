FROM python:3.8-slim

WORKDIR /app

# Copy requirements from root
COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 