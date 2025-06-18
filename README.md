# Amused Chatbot

A Rasa-based chatbot with FastAPI integration, deployed on Render.

## Project Structure

```
amused/
├── api/                    # FastAPI server
│   └── main.py
├── actions/               # Rasa custom actions
│   ├── requirements.txt
│   ├── __init__.py
│   └── actions.py
├── data/                  # Rasa training data
│   ├── nlu.yml
│   ├── rules.yml
│   └── stories.yml
├── config.yml            # Rasa configuration
├── credentials.yml       # Rasa credentials
├── domain.yml           # Rasa domain
├── endpoints.yml        # Rasa endpoints
├── requirements.txt     # Python dependencies
├── app.py              # Main FastAPI application
├── render.yaml         # Render deployment config
└── runtime.txt         # Python runtime version
```

## Deployment

This project is configured for deployment on Render using Python. The deployment consists of a single service:

1. FastAPI Server (Port 10000)

### Deployment Steps

1. Push your code to a Git repository
2. Create a new Web Service on Render
3. Connect your repository
4. Render will automatically deploy using the `render.yaml` configuration

### Environment Variables

The following environment variables are configured:

- `RASA_API_URL`: URL of the Rasa server
- `PORT`: Service port (default: 10000)

## Development

### Local Development

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   python app.py
   ```

### Testing

- FastAPI: http://localhost:10000/api/health
- API Documentation: http://localhost:10000/docs 