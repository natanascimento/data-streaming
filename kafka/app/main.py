import asyncio

from app.core.config import settings
from app.core.config.kafka import KafkaClient, KafkaConsumer, KafkaProducer
from app.controller.topic import TopicController
from app.data.consumer import DataConsumer
from app.data.producer import DataProducer
from app.model.purchase import Purchase


async def produce(topic_name):
    """Runs the Producer tasks"""
    for i in range(10000):
        await DataProducer.produce(producer=KafkaProducer.get(broker_configs=settings.kafka_broker),
                                   topic_name=topic_name,
                                   message=Purchase.get())

async def consume(topic_name):
    """Runs the Consumer tasks"""
    await DataConsumer.consume(consumer=KafkaConsumer.get(broker_configs=settings.kafka_broker,
                                                          consumer_config={"group.id":"0"}),
                                                          topic_name=topic_name)

async def produce_consume(topic_name):
    produce_task = asyncio.create_task(produce(topic_name=topic_name))
    consume_task = asyncio.create_task(consume(topic_name=topic_name))

    await produce_task
    await consume_task

def start():
    kafka_client = KafkaClient.get(broker_configs=settings.kafka_broker)
    topic_name = "com.natanascimento.lesson.teste"
    topic_controller = TopicController(client=kafka_client)
    topic_exists = topic_controller.topic_exists(topic_name=topic_name)

    if not topic_exists:
        print(f"Topic {topic_name} doesn't exists")
        topic_controller.create(topic_name=topic_name)

    asyncio.run(produce_consume(topic_name=topic_name))