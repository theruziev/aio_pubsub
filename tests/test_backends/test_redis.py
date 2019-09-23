import aioredis
import pytest

from aio_pubsub.backends.redis import RedisPubSub


@pytest.fixture
async def create_pub_sub_conn():
    pub = await aioredis.create_redis("redis://localhost:6379/0?encoding=utf-8")
    sub = await aioredis.create_redis("redis://localhost:6379/0?encoding=utf-8")
    yield pub, sub
    pub.close()
    sub.close()


@pytest.mark.asyncio
async def test_subscriber_isinstance(create_pub_sub_conn):
    from aio_pubsub.backends.redis import RedisSubscriber

    pubsub = RedisPubSub(*create_pub_sub_conn)
    subscriber = await pubsub.subscribe("a_chan")
    assert isinstance(subscriber, RedisSubscriber)


@pytest.mark.asyncio
async def test_iteration_protocol(create_pub_sub_conn):
    pubsub = RedisPubSub(*create_pub_sub_conn)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"


@pytest.mark.asyncio
async def test_pubsub(create_pub_sub_conn):
    pubsub = RedisPubSub(*create_pub_sub_conn)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("a_chan", "hello universe!")
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_not_subscribed_chan(create_pub_sub_conn):
    pubsub = RedisPubSub(*create_pub_sub_conn)
    subscriber_a_chan = await pubsub.subscribe("a_chan")
    subscriber_c_chan = await pubsub.subscribe("c_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("b_chan", "junk message")
    await pubsub.publish("c_chan", "hello universe!")
    assert await subscriber_a_chan.__anext__() == "hello world!"
    assert await subscriber_c_chan.__anext__() == "hello universe!"
