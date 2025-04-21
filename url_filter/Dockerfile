FROM python:3.9-slim
WORKDIR /app
COPY kafka_base.py .
COPY url_filter/url_filter.py ./url_filter.py
RUN pip install --no-cache-dir confluent-kafka python-dotenv
CMD ["python", "url_filter.py"]