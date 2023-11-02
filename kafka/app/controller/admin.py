from confluent_kafka.admin import NewTopic, ClusterMetadata

from app.core.config.kafka import KafkaClient


class TopicController:

    def __init__(self, client: KafkaClient):
        self._client = client
    
    @property
    def topics_metadata(self) -> ClusterMetadata:
        return self._client.list_topics()

    def topic_exists(self, topic_name: str) -> bool:
        return self.topics_metadata.topics.get(topic_name) is not None

    def list_topics(self) -> list:
        return list(self.topics_metadata.topics.keys())
    
    def create(self, topic_name: str) -> bool:
        futures = self._client.create_topics(
            [
                NewTopic(
                    topic=topic_name,
                    num_partitions=5,
                    replication_factor=1,
                    config={
                        "cleanup.policy": "compact",
                        "compression.type": "lz4",
                        "retention.ms": -1,
                        "file.delete.delay.ms": 100,
                        "delete.retention.ms": 100
                    }
                )
            ]
        )

        for topic, future in futures.items():
            try:
                print(f"{topic} created")
            except Exception as e:
                print(f"failed to create topic {topic_name}: {e}")
                raise e