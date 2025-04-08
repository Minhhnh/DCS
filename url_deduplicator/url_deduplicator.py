# url_deduplicator.py
import binascii
from kafka_base import KafkaConsumer, KafkaProducer


class URLDeduplicator:
    def __init__(self):
        self.consumer = KafkaConsumer(topic="urls_to_deduplicate", group_id="url_deduplicator")
        self.producer = KafkaProducer(topic="deduplicated_urls")
        self.seen_hashes = set()

    def deduplicate(self, url: str) -> bool:
        crc32_hash = binascii.crc32(url.encode("utf-8")) & 0xFFFFFFFF
        crc32_hex = format(crc32_hash, "08x")
        if crc32_hex in self.seen_hashes:
            return False
        self.seen_hashes.add(crc32_hex)
        return True

    def run(self):
        for message in self.consumer.consume():
            url = message["url"]
            print(f"Deduplicating URL: {url}")
            if self.deduplicate(url):
                self.producer.produce({"url": url})


if __name__ == "__main__":
    deduplicator = URLDeduplicator()
    deduplicator.run()
