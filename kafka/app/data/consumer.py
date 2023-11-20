import asyncio

from app.core.config.kafka import KafkaConsumer
from app.exceptions.kafka import ConsumerError


class DataConsumer:

    def _get_assignment(consumer, partitions) -> None:
        print(f'assigment:{partitions}')

    async def consume(consumer: KafkaConsumer, topic_name: str) -> dict:
        """Consumes data from the Kafka Topic"""
        try:
            consumer.subscribe([topic_name], on_assign=DataConsumer._get_assignment)
    
            while True:
                message = consumer.poll(timeout=1.0)

                if message is not None:
                    print(f"""Consumed message with key:{message.key()} | 
                                                    value:{message.value()} | 
                                                    headers:{message.headers()} | 
                                                    latency:{message.latency()} | 
                                                    offset:{message.offset()} |
                                                    timestamp:{message.timestamp()}""")

                print("No message received by consumer")

                await asyncio.sleep(0.01)
                
        except Exception as e:
            raise e

        finally:
            consumer.close()