import asyncio
import uuid

from app.core.config.kafka import KafkaProducer


class DataProducer:

    def _delivery_callback(error, msg) -> None:
        if error:
            print(f'Message failed delivery: {error}\n')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}] @ {msg.offset()}\n')

    async def produce(producer: KafkaProducer, message: dict|str, topic_name: str) -> dict:
        """Produces data into the Kafka Topic"""
        try:
            producer.produce(topic=topic_name,
                             key=str(uuid.uuid4()),
                             value=str(message), 
                             on_delivery=DataProducer._delivery_callback)
            producer.poll(0)
            await asyncio.sleep(0.1)
        except BufferError:
            print(f'Local producer queue is full ({len(producer)} messages awaiting delivery): try again\n')
        except Exception as exception:
            print(exception)

        producer.flush()