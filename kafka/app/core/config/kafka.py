from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient

from app.core.config.settings import KafkaBroker


class KafkaClient:
    
    @staticmethod
    def get(broker_configs: KafkaBroker) -> AdminClient:
        """Get kafka client"""
        return AdminClient({"bootstrap.servers": broker_configs.url})


class KafkaProducer:

    @staticmethod
    def get(broker_configs: KafkaBroker) -> Producer:
        """Define a kafka producer"""
        return Producer({"bootstrap.servers": broker_configs.url})


class KafkaConsumer:

    @staticmethod
    def get(broker_configs: KafkaBroker, consumer_config: dict) -> Consumer:
        """Define a kafka consumer"""
        broker_configs = {"bootstrap.servers": broker_configs.url}
        return Consumer({**broker_configs, **consumer_config})
