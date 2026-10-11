from kraken_api.mock import KrakenMockAPI
from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    kraken_api: KrakenMockAPI | KrakenWebsocketAPI,
):
    """
    It does 2 things:
    1. Reads trades from the Kraken API
    2. Pushes them to a Kafka topic

    Args:
        kafka_broker_address: str
        kafka_topic: str

    Returns:
        None
    """
    logger.info("Start the trades service")

    app = Application(broker_address=kafka_broker_address)

    topic = app.topic(name=kafka_topic, value_serializer="json")

    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()

            for trade in trades:
                # push this trade to a Kafka topic
                # TODO

                message = topic.serialize(
                    key=trade.pair.replace("/", "-"), value=trade.to_dict()
                )

                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.info(f"Pushed trade to Kafka: {trade}")


if __name__ == "__main__":
    from config import config

    kraken_api = KrakenWebsocketAPI(pairs=config.pairs)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        kraken_api=kraken_api,
    )
