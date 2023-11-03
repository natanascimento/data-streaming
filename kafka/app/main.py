from app.core.config import settings
from app.core.config.kafka import KafkaClient, KafkaConsumer
from app.controller.topic import TopicController


def main():
    kafka_client = KafkaClient.get(settings.kafka_broker)
    topic_name = "com.natanascimento.lesson.teste"
    topic_controller = TopicController(client=kafka_client)
    topic_exists = topic_controller.topic_exists(topic_name=topic_name)
    
    print(KafkaConsumer.get(broker_configs=settings.kafka_broker,
                      consumer_config={"group.id":"0"}))