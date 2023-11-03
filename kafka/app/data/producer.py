from app.core.config.kafka import KafkaProducer


class DataProducer:

    def produce(producer: KafkaProducer, topic_name: str) -> dict:
        """Produces data into the Kafka Topic"""
        raise NotImplemented