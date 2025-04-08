FROM python:3.9-slim
WORKDIR /app
COPY ../kafka_base/kafka_base.py .
COPY url_filter.py .
RUN pip install --no-cache-dir confluent-kafka
CMD ["python", "url_filter.py"]