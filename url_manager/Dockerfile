# Use a lightweight Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the shared kafka_base module
COPY kafka_base.py .

# Copy the service code
COPY url_manager/url_manager.py ./url_manager.py

# Install dependencies
RUN pip install --no-cache-dir confluent-kafka python-dotenv

# Command to run the service
CMD ["python", "url_manager.py"]