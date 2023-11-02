from dataclasses import dataclass


@dataclass
class KafkaBroker:
    protocol: str = "PLAINTEXT"
    host: str = "localhost"
    port: str = "9092"
    url: str = None

    def __post_init__(self):
        self.url = f"{self.protocol}://{self.host}:{self.port}"

@dataclass
class Settings:
    kafka_broker: KafkaBroker = KafkaBroker()