# html_downloader.py
import requests
from kafka_base import KafkaConsumer, KafkaProducer


class HTMLDownloader:
    def __init__(self):
        self.consumer = KafkaConsumer(topic="deduplicated_urls", group_id="html_downloader")
        self.producer = KafkaProducer(topic="downloaded_documents")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def download(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except (requests.RequestException, Exception) as e:
            print(f"Error downloading {url}: {e}")
            return ""

    def run(self):
        for message in self.consumer.consume():
            url = message["url"]
            print(f"Downloading URL: {url}")
            html_content = self.download(url)
            if html_content:
                self.producer.produce({"url": url, "content": html_content})


if __name__ == "__main__":
    downloader = HTMLDownloader()
    downloader.run()
