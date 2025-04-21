FROM python:3.9-slim
WORKDIR /app
COPY kafka_base.py .
COPY document_extractor/document_extractor.py ./document_extractor.py
RUN pip install --no-cache-dir confluent-kafka beautifulsoup4 python-dotenv
CMD ["python", "document_extractor.py"]