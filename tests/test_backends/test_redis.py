import pytest

from aio_pubsub.backends.redis import RedisPubSub


@pytest.mark.asyncio
async def test_subscriber_isinstance():
    from aio_pubsub.backends.redis import RedisSubscriber

    pubsub = RedisPubSub()
    await pubsub.init()
    subscriber = await pubsub.subscribe("a_chan")
    assert isinstance(subscriber, RedisSubscriber)
    await pubsub.close()


@pytest.mark.asyncio
async def test_iteration_protocol():
    pubsub = RedisPubSub()
    await pubsub.init()
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"
    await pubsub.close()


@pytest.mark.asyncio
async def test_pubsub():
    pubsub = RedisPubSub()
    await pubsub.init()
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("a_chan", "hello universe!")
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"
    await pubsub.close()


@pytest.mark.asyncio
async def test_not_subscribed_chan():
    pubsub = RedisPubSub()
    await pubsub.init()
    subscriber_a_chan = await pubsub.subscribe("a_chan")
    subscriber_c_chan = await pubsub.subscribe("c_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("b_chan", "junk message")
    await pubsub.publish("c_chan", "hello universe!")
    assert await subscriber_a_chan.__anext__() == "hello world!"
    assert await subscriber_c_chan.__anext__() == "hello universe!"
    await pubsub.close()
