from app.core.config import settings
from app.core.config.kafka import KafkaClient
from app.controller.admin import TopicController


def main():
    kafka_client = KafkaClient.get(settings.kafka_broker)
    topic_name = "com.natanascimento.lesson.asdasdas"
    topic_exists = TopicController(client=kafka_client).topic_exists(topic_name=topic_name)
    topic_exists = TopicController(client=kafka_client).get_topics()
    print(topic_exists.__dict__)
    print(topic_exists.topics)