import aioredis
import pytest

from aio_pubsub.backends.redis import RedisPubSub


@pytest.fixture
async def create_conn():
    pub = await aioredis.create_redis("redis://localhost:6379/0?encoding=utf-8")
    yield pub
    pub.close()

@pytest.mark.asyncio
async def test_subscriber_isinstance(create_conn):
    from aio_pubsub.backends.redis import RedisSubscriber

    pubsub = RedisPubSub(create_conn)
    subscriber = await pubsub.subscribe("a_chan")
    assert isinstance(subscriber, RedisSubscriber)


@pytest.mark.asyncio
async def test_iteration_protocol(create_conn):
    pubsub = RedisPubSub(create_conn)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"


@pytest.mark.asyncio
async def test_pubsub(create_conn):
    pubsub = RedisPubSub(create_conn)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("a_chan", "hello universe!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_not_subscribed_chan(create_conn):
    pubsub = RedisPubSub(create_conn)
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
async def test_broadcast(create_conn):
    pubsub = RedisPubSub(create_conn)
    subscriber_1 = await pubsub.subscribe("a_chan")
    subscriber_2 = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber_1 = subscriber_1.__aiter__()
    subscriber_2 = subscriber_2.__aiter__()
    assert await subscriber_1.__anext__() == "hello world!"
    assert await subscriber_2.__anext__() == "hello world!"
