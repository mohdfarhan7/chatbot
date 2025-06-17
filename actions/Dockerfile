FROM rasa/rasa-sdk:3.6.16

# Copy actions code
COPY . /app/actions

# Install additional dependencies if needed
RUN pip install -r /app/actions/requirements.txt

# Expose the port
EXPOSE 5055

# Start the action server
CMD ["start", "--actions", "actions"] 