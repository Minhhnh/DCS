FROM python:3.9-slim
WORKDIR /app
COPY ../kafka_base/kafka_base.py .
COPY html_downloader.py .
RUN pip install --no-cache-dir confluent-kafka requests
CMD ["python", "html_downloader.py"]