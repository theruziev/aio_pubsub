import pytest

from async_pubsub.backends.mongodb import MongoPubSub


@pytest.mark.asyncio
async def test_subscriber_isinstance():
    from async_pubsub.backends.mongodb import MongoSubscriber

    pubsub = MongoPubSub()
    await pubsub.init()
    subscriber = await pubsub.subscribe("a_chan")
    assert isinstance(subscriber, MongoSubscriber)


@pytest.mark.asyncio
async def test_iteration_protocol():
    pubsub = MongoPubSub()
    await pubsub.init()
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber = await subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"


@pytest.mark.asyncio
async def test_pubsub():
    pubsub = MongoPubSub()
    await pubsub.init()
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("a_chan", "hello universe!")
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_subscribe_multiple_chan():
    pubsub = MongoPubSub()
    await pubsub.init()
    subscriber = await pubsub.subscribe("a_chan", "b_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("b_chan", "hello universe!")
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_not_subscribed_chan():
    pubsub = MongoPubSub()
    await pubsub.init()
    subscriber = await pubsub.subscribe("a_chan", "c_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("b_chan", "junk message")
    await pubsub.publish("c_chan", "hello universe!")
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"
