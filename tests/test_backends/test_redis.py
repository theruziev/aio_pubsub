import aioredis
import pytest

from aio_pubsub.backends.redis import RedisPubSub


@pytest.fixture
async def redis_url():
    url = "redis://localhost:6379/0?encoding=utf-8"
    yield url

@pytest.mark.asyncio
async def test_subscriber_isinstance(redis_url):
    from aio_pubsub.backends.redis import RedisSubscriber

    pubsub = RedisPubSub(redis_url)
    subscriber = await pubsub.subscribe("a_chan")
    assert isinstance(subscriber, RedisSubscriber)


@pytest.mark.asyncio
async def test_iteration_protocol(redis_url):
    pubsub = RedisPubSub(redis_url)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"


@pytest.mark.asyncio
async def test_pubsub(redis_url):
    pubsub = RedisPubSub(redis_url)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("a_chan", "hello universe!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_not_subscribed_chan(redis_url):
    pubsub = RedisPubSub(redis_url)
    subscriber_a_chan = await pubsub.subscribe("a_chan")
    subscriber_c_chan = await pubsub.subscribe("c_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("b_chan", "junk message")
    await pubsub.publish("c_chan", "hello universe!")
    subscriber_a_chan = subscriber_a_chan.__aiter__()
    subscriber_c_chan = subscriber_c_chan.__aiter__()
    assert await subscriber_a_chan.__anext__() == "hello world!"
    assert await subscriber_c_chan.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_broadcast(redis_url):
    pubsub = RedisPubSub(redis_url)
    subscriber_1 = await pubsub.subscribe("a_chan")
    subscriber_2 = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber_1 = subscriber_1.__aiter__()
    subscriber_2 = subscriber_2.__aiter__()
    assert await subscriber_1.__anext__() == "hello world!"
    assert await subscriber_2.__anext__() == "hello world!"
