# url_manager.py
from kafka_base import KafkaProducer


class URLManager:
    def __init__(self):
        self.producer = KafkaProducer(topic="urls_to_deduplicate")
        self.url_db = ["https://example.com"]  # Seed URLs

    def run(self):
        for url in self.url_db:
            print(f"Producing URL: {url}")
            self.producer.produce({"url": url})


if __name__ == "__main__":
    manager = URLManager()
    manager.run()
