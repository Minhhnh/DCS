FROM python:3.9-slim
WORKDIR /app
COPY kafka_base.py .
COPY html_downloader/html_downloader.py ./html_downloader.py
RUN pip install --no-cache-dir confluent-kafka requests python-dotenv
CMD ["python", "html_downloader.py"]