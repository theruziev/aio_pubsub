import json

from aio_pubsub.interfaces import PubSub, Subscriber
from aio_pubsub.typings import Message

aioredis_installed = False
try:
    import aioredis 

    aioredis_installed = True
except ImportError:
    pass  # pragma: no cover


class RedisSubscriber(Subscriber):
    def __init__(self, sub, channel):
        self.sub = sub
        self.channel = channel

    def __aiter__(self):
        return self.channel.iter(encoding="utf-8", decoder=json.loads)


class RedisPubSub(PubSub):
    def __init__(self, url: str) -> None:
        if aioredis_installed is False:
            raise RuntimeError("Please install `aioredis`")  # pragma: no cover

        self.url = url
        self.connection = None

    async def publish(self, channel: str, message: Message) -> None:
        if self.connection is None:
            self.connection = await aioredis.create_redis(self.url)

            
        channels = await self.connection.pubsub_channels(channel)
        for ch in channels:
            await self.connection.publish_json(ch, message)

    async def subscribe(self, channel) -> "RedisSubscriber":
        if aioredis_installed is False:
            raise RuntimeError("Please install `aioredis`")  # pragma: no cover

        sub = await aioredis.create_redis(self.url)

        channel = await sub.subscribe(channel)
        return RedisSubscriber(sub, channel[0])
