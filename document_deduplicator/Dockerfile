FROM python:3.9-slim

WORKDIR /app

# Copy the shared kafka_base module
COPY kafka_base.py .

# Copy the service code
COPY document_deduplicator/document_deduplicator.py ./document_deduplicator.py

# Install dependencies
RUN pip install --no-cache-dir confluent-kafka redis google-cloud-storage python-dotenv

# Command to run the service
CMD ["python", "document_deduplicator.py"]