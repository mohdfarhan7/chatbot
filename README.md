# Amused Chatbot Deployment Guide

This guide provides instructions for deploying the Amused chatbot on a Linux server.

## Prerequisites

- Ubuntu/Debian-based server
- SSH access with sudo privileges
- Domain name (aitechnotech.in) pointing to the server

## Deployment Steps

1. **Connect to the server**
   ```bash
   ssh aitechnotech@168.231.69.44
   ```

2. **Clone the repository**
   ```bash
   cd /home/aitechnotech
   git clone <repository-url> amused
   cd amused
   ```

3. **Make the deployment script executable**
   ```bash
   chmod +x deploy.sh
   ```

4. **Run the deployment script**
   ```bash
   ./deploy.sh
   ```

## Service Management

- **Check FastAPI service status**
  ```bash
  sudo systemctl status amused-api
  ```

- **Restart FastAPI service**
  ```bash
  sudo systemctl restart amused-api
  ```

- **Check Docker containers**
  ```bash
  docker-compose ps
  ```

- **View logs**
  ```bash
  # FastAPI logs
  sudo journalctl -u amused-api

  # Docker logs
  docker-compose logs -f
  ```

## Ports Used

- 80: Nginx (HTTP)
- 8000: FastAPI Server
- 5005: Rasa Server
- 5055: Action Server

## Environment Variables

The following environment variables are used:
- `RASA_API_URL`: URL of the Rasa server (default: http://localhost:5005)
- `PORT`: Port for the FastAPI server (default: 8000)

## Troubleshooting

1. If the FastAPI service fails to start:
   ```bash
   sudo journalctl -u amused-api -n 50
   ```

2. If Docker containers fail to start:
   ```bash
   docker-compose logs
   ```

3. If Nginx fails to start:
   ```bash
   sudo nginx -t
   sudo systemctl status nginx
   ```

## Security Notes

- The server is configured to use HTTP. For production, please set up SSL/TLS certificates using Let's Encrypt.
- Update the default passwords and credentials in the configuration files.
- Regularly update the system and dependencies. 