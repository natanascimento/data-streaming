import asyncio
import argparse

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

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help="mode that you'll use to interact with kafka (possible args: consume | produce)")
    parser.add_argument('-t', '--topic', help="topic that you'll interact")
    args = parser.parse_args()
    if not args.topic:
        raise ValueError("It's necessary to have a topic to consume or produce data")
    if args.mode != "consume" and args.mode != "produce" and args.mode != None:
        raise ValueError("It's necessary to have 'consume' or 'produce' for mode argument")
    return args

def start():
    args = get_arguments()
    kafka_client = KafkaClient.get(broker_configs=settings.kafka_broker)
    topic_controller = TopicController(client=kafka_client)
    topic_exists = topic_controller.topic_exists(topic_name=args.topic)

    if not topic_exists:
        print(f"Topic {args.topic} doesn't exists")
        topic_controller.create(topic_name=args.topic)

    if args.mode == "consume":
        asyncio.run(consume(topic_name=args.topic))
    elif args.mode == "produce":
        asyncio.run(produce(topic_name=args.topic))

    asyncio.run(produce_consume(topic_name=args.topic))