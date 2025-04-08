# url_filter.py
from urllib.parse import urlparse
from kafka_base import KafkaConsumer, KafkaProducer


class URLFilter:
    def __init__(self):
        self.consumer = KafkaConsumer(topic="extracted_urls", group_id="url_filter")
        self.producer = KafkaProducer(topic="urls_to_deduplicate")
        self.config_db = {"hosts": ["example.com"], "prefixes": ["https://example.com"], "patterns": ["*.jpg", "*.png"]}

    def filter(self, url: str) -> bool:
        parsed_url = urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path

        allowed_hosts = self.config_db.get("hosts", [])
        if allowed_hosts and host not in allowed_hosts:
            return False

        prefixes = self.config_db.get("prefixes", [])
        if prefixes and not any(url.startswith(prefix) for prefix in prefixes):
            return False

        patterns = self.config_db.get("patterns", [])
        if patterns and any(url.endswith(pattern.lstrip("*")) for pattern in patterns):
            return False

        return True

    def run(self):
        for message in self.consumer.consume():
            url = message["url"]
            print(f"Filtering URL: {url}")
            if self.filter(url):
                self.producer.produce({"url": url})


if __name__ == "__main__":
    url_filter = URLFilter()
    url_filter.run()
