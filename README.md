# Amused Chatbot

A Rasa-based chatbot with FastAPI integration, deployed on Render.

## Project Structure

```
amused/
├── api/                    # FastAPI server
│   ├── Dockerfile
│   └── main.py
├── actions/               # Rasa custom actions
│   ├── Dockerfile
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
├── Dockerfile          # Main Docker configuration
├── docker-compose.yml  # Docker services
├── render.yaml         # Render deployment config
├── runtime.txt         # Python runtime version
├── .dockerignore      # Docker build exclusions
└── .gitignore         # Git exclusions
```

## Deployment

This project is configured for deployment on Render using Docker containers. The deployment consists of three services:

1. Rasa Server (Port 5005)
2. Action Server (Port 5055)
3. FastAPI Server (Port 8034)

### Deployment Steps

1. Push your code to a Git repository
2. Create a new Blueprint on Render
3. Connect your repository
4. Render will automatically deploy all services using the `render.yaml` configuration

### Environment Variables

The following environment variables are configured:

- `RASA_API_URL`: URL of the Rasa server
- `RASA_ACTIONS_URL`: URL of the Action server
- `PORT`: Service port (varies by service)

## Development

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start services using Docker Compose:
   ```bash
   docker-compose up
   ```

### Testing

- FastAPI: http://localhost:8034/api/health
- Rasa: http://localhost:5005/status
- Action Server: http://localhost:5055/health 