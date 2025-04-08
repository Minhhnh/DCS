FROM python:3.9-slim
WORKDIR /app
COPY ../kafka_base/kafka_base.py .
COPY document_extractor.py .
RUN pip install --no-cache-dir confluent-kafka beautifulsoup4
CMD ["python", "document_extractor.py"]