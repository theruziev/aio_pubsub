import json
from aio_pubsub.interfaces import PubSub, Subscriber

aioredis_installed = False
try:
    import aioredis

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
    def __init__(self, dsn="redis://localhost:6379/0?encoding=utf-8", timeout=10):
        if aioredis_installed is False:
            raise RuntimeError("Please install `aioredis`")  # pragma: no cover
        self.dsn = dsn
        self.sub = None
        self.pub = None
        self.timeout = timeout

    async def init(self):
        self.sub = await aioredis.create_redis(self.dsn, timeout=self.timeout)
        self.pub = await aioredis.create_redis(self.dsn, timeout=self.timeout)

    async def publish(self, channel, message):
        channels = await self.pub.pubsub_channels(channel)
        for ch in channels:
            await self.pub.publish_json(ch, message)

    async def subscribe(self, channel):
        channel = await self.sub.subscribe(channel)
        return RedisSubscriber(channel[0])

    async def close(self):
        self.sub.close()
        self.pub.close()
