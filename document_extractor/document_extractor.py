# document_extractor.py
from bs4 import BeautifulSoup
from kafka_base import KafkaConsumer, KafkaProducer


class DocumentExtractor:
    def __init__(self):
        self.consumer = KafkaConsumer(topic="unique_documents", group_id="doc_extractor")
        self.producer = KafkaProducer(topic="extracted_urls")

    def extract_urls(self, document: str) -> list:
        if not document:
            return []
        soup = BeautifulSoup(document, "html.parser")
        urls = []
        for link in soup.find_all("a", href=True):
            url = link["href"]
            if url.startswith("http"):
                urls.append(url)
        return urls

    def run(self):
        for message in self.consumer.consume():
            url = message["url"]
            document = message["content"]
            print(f"Extracting URLs from: {url}")
            new_urls = self.extract_urls(document)
            for new_url in new_urls:
                self.producer.produce({"url": new_url})


if __name__ == "__main__":
    extractor = DocumentExtractor()
    extractor.run()
