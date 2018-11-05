import aio_pika
from aio_pika import ExchangeType

from async_pubsub.interfaces import PubSub, Subscriber
from urllib.parse import urlparse
from queue import Queue


class AmqpSubscriber(Subscriber):
    def __init__(self, amqp_chan, exchanges):
        self.channel = amqp_chan
        self.messages = Queue(maxsize=0)
        self.exchanges = exchanges
        self.queue = None

    async def init(self):
        pass

    async def __aiter__(self):
        return self

    async def __anext__(self):
        pass


class AmqpPubSub(PubSub):
    def __init__(self, dsn):
        self.dsn = dsn
        self.connection = None
        self.channel = None
        self.exchange = None
        self.exchange_name = "pb_exchange"

    async def init(self):
        self.connection = await aio_pika.connect_robust(self.dsn)

        async with self.connection:
            # Creating channel
            self.channel = await self.connection.channel()

    async def _declare_exchanges(self, *channels):
        exchanges = []
        for channel in channels:
            exchanges.append(self.channel.declare_exchange(channel, type=ExchangeType.FANOUT))
        return exchanges

    async def subscribe(self, *channels):
        exchanges = await self._declare_exchanges(*channels)
        return AmqpSubscriber(self.channel, exchanges)

    async def publish(self, channel, message):
        await self._declare_exchanges(self.channel, channel)
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message), routing_key=channel
        )
