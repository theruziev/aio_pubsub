import json

from aio_pubsub.interfaces import PubSub, Subscriber
from aio_pubsub.typings import Message

aioredis_installed = False
try:
    from aioredis import Redis

    aioredis_installed = True
except ImportError:
    pass  # pragma: no cover


class RedisSubscriber(Subscriber):
    def __init__(self, channel):
        self.channel = channel

    def __aiter__(self):
        return self

    async def __anext__(self):
        async for msg in self.channel.iter(encoding="utf-8", decoder=json.loads):
            return msg


class RedisPubSub(PubSub):
    def __init__(self, pub_connection: Redis, sub_connection: Redis):
        if aioredis_installed is False:
            raise RuntimeError("Please install `aioredis`")  # pragma: no cover

        self.sub = pub_connection
        self.pub = sub_connection

    async def publish(self, channel: str, message: Message):
        channels = await self.pub.pubsub_channels(channel)
        for ch in channels:
            await self.pub.publish_json(ch, message)

    async def subscribe(self, channel) -> "RedisSubscriber":
        channel = await self.sub.subscribe(channel)
        return RedisSubscriber(channel[0])
