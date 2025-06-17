#!/bin/bash

# Exit on error
set -e

echo "Starting deployment..."

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
echo "Installing system dependencies..."
sudo apt-get install -y python3.8 python3.8-venv python3-pip docker.io nginx

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Start and enable Docker
echo "Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
echo "Adding user to docker group..."
sudo usermod -aG docker $USER

# Create virtual environment
echo "Setting up Python virtual environment..."
python3.8 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install wheel setuptools
pip install -r requirements.txt

# Verify Rasa installation
echo "Verifying Rasa installation..."
rasa --version

# Build and start Docker containers
echo "Starting Docker containers..."
docker-compose up -d --build

# Create systemd service file
echo "Setting up FastAPI service..."
sudo tee /etc/systemd/system/amused-api.service << 'EOF'
[Unit]
Description=Amused FastAPI Server
After=network.target

[Service]
User=aitechnotech
WorkingDirectory=/home/aitechnotech/amused/chatbot
Environment="PATH=/home/aitechnotech/amused/chatbot/venv/bin"
ExecStart=/home/aitechnotech/amused/chatbot/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8034

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
echo "Starting FastAPI service..."
sudo systemctl daemon-reload
sudo systemctl enable amused-api
sudo systemctl start amused-api

# Configure Nginx
echo "Configuring Nginx..."
sudo tee /etc/nginx/sites-available/amused << 'EOF'
server {
    listen 80;
    server_name aitechnotech.in;

    location / {
        proxy_pass http://localhost:8034;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /webhooks/rest/webhook {
        proxy_pass http://localhost:5005;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable the site
echo "Enabling Nginx site..."
sudo ln -sf /etc/nginx/sites-available/amused /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo "Deployment completed successfully!"

# Print status
echo "Checking service status..."
echo "FastAPI service status:"
sudo systemctl status amused-api
echo "Docker containers status:"
docker-compose ps
echo "Nginx status:"
sudo systemctl status nginx

# Test the API
echo "Testing API endpoint..."
curl -v http://localhost:8034/api/health 