FROM python:3.9-slim
WORKDIR /app
COPY kafka_base.py .
COPY url_deduplicator/url_deduplicator.py ./url_deduplicator.py
RUN pip install --no-cache-dir confluent-kafka python-dotenv
CMD ["python", "url_deduplicator.py"]