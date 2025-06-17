#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required system packages
sudo apt-get install -y python3.8 python3.8-venv python3-pip docker.io docker-compose nginx

# Create virtual environment
python3.8 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Build and start Docker containers
docker-compose up -d --build

# Set up systemd service for the FastAPI server
sudo tee /etc/systemd/system/amused-api.service << EOF
[Unit]
Description=Amused FastAPI Server
After=network.target

[Service]
User=aitechnotech
WorkingDirectory=/home/aitechnotech/amused/chatbot
Environment="PATH=/home/aitechnotech/amused/chatbot/venv/bin"
ExecStart=/home/aitechnotech/amused/chatbot/venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl enable amused-api
sudo systemctl start amused-api

# Configure Nginx
sudo tee /etc/nginx/sites-available/amused << EOF
server {
    listen 80;
    server_name aitechnotech.in;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /webhooks/rest/webhook {
        proxy_pass http://localhost:5005;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/amused /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

echo "Deployment completed successfully!" 