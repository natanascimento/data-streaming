from confluent_kafka.admin import AdminClient

from app.core.config.settings import KafkaBroker


class KafkaClient:
    
    @staticmethod
    def get(broker_configs: KafkaBroker) -> AdminClient:
        return AdminClient({"bootstrap.servers": broker_configs.url})
