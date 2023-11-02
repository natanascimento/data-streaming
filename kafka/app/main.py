from app.core.config import settings
from app.core.config.kafka import KafkaClient
from app.controller.admin import TopicController


def main():
    kafka_client = KafkaClient.get(settings.kafka_broker)
    topic_name = "com.natanascimento.lesson.teste"
    topic_controller = TopicController(client=kafka_client)
    topic_exists = topic_controller.topic_exists(topic_name=topic_name)
    if not topic_exists:
        topic_controller.create(topic_name=topic_name)

    print()
    print(topic_controller.list_topics())