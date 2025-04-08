import hashlib
import os
import redis
from google.cloud import storage
from kafka_base import KafkaConsumer, KafkaProducer


class DocumentDeduplicator:
    def __init__(self):
        self.consumer = KafkaConsumer(topic="downloaded_documents", group_id="doc_deduplicator")
        self.producer = KafkaProducer(topic="unique_documents")

        # Connect to Redis
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"), port=int(os.getenv("REDIS_PORT", "6379")), decode_responses=True
        )

        # Initialize GCS client
        self.gcs_client = storage.Client()
        self.bucket = self.gcs_client.bucket(os.getenv("GCS_BUCKET", "crawler-documents"))

    def deduplicate(self, url: str, document: str) -> bool:
        # Compute SHA-256 hash
        sha256_hash = hashlib.sha256(document.encode("utf-8")).hexdigest()

        # Check if document exists in Redis
        if self.redis_client.exists(sha256_hash):
            return False  # Document is a duplicate

        # Mark the document as seen in Redis
        self.redis_client.set(sha256_hash, 1)

        # Store the document in GCS
        # Use the SHA-256 hash as the object name to ensure uniqueness
        blob = self.bucket.blob(f"documents/{sha256_hash}.json")
        blob.upload_from_string(f'{{"url": "{url}", "content": "{document}"}}', content_type="application/json")
        print(f"Stored document in GCS: {sha256_hash}.json")
        return True  # Document is unique

    def run(self):
        for message in self.consumer.consume():
            url = message["url"]
            document = message["content"]
            print(f"Deduplicating document from: {url}")
            if self.deduplicate(url, document):
                self.producer.produce({"url": url, "content": document})


if __name__ == "__main__":
    deduplicator = DocumentDeduplicator()
    deduplicator.run()
