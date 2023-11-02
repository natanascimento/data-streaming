from confluent_kafka.admin import NewTopic

from app.core.config.kafka import KafkaClient


class TopicController:

    def __init__(self, client: KafkaClient):
        self.__client = client

    def topic_exists(self, topic_name: str) -> bool:
        if self.__client.list_topics(topic=topic_name):
            return True
        return False

    def get_topics(self):
        return self.__client.list_topics()
    
    def create(self) -> bool:
        raise NotImplemented