#!/bin/bash

# Remove unnecessary directories
rm -rf tests/
rm -rf trial/
rm -rf chatbot/
rm -rf env/
rm -rf venv/
rm -rf .rasa/
rm -rf models/

# Remove unnecessary files
rm -f deploy.sh
rm -f Procfile

# Clean Python cache files
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

# Clean up any temporary files
find . -type f -name "*.log" -delete
find . -type f -name "*.tmp" -delete

echo "Cleanup completed successfully!" 