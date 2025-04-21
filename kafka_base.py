import json
from confluent_kafka import Producer, Consumer, KafkaError
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class KafkaProducer:
    def __init__(self, topic: str):
        bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")
        self.topic = topic
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

    def produce(self, message: dict):
        self.producer.produce(self.topic, value=json.dumps(message).encode("utf-8"))
        self.producer.flush()


class KafkaConsumer:
    def __init__(self, topic: str, group_id: str):
        bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS", "localhost:9092")
        self.topic = topic
        self.consumer = Consumer(
            {"bootstrap.servers": bootstrap_servers, "group.id": group_id, "auto.offset.reset": "earliest"}
        )
        self.consumer.subscribe([topic])

    def consume(self):
        while True:
            msg = self.consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break
            yield json.loads(msg.value().decode("utf-8"))
