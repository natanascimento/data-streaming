from app.core.config.kafka import KafkaConsumer


class DataProducer:

    def produce(consumer: KafkaConsumer, topic_name: str) -> dict:
        """Consumes data from the Kafka Topic"""
        raise NotImplemented