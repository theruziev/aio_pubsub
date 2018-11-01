import pytest

from async_pubsub.backends.memory import MemoryPubSub


@pytest.mark.asyncio
async def test_iteration_protocol():
    pubsub = MemoryPubSub()
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber = await subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"


@pytest.mark.asyncio
async def test_pubsub():
    pubsub = MemoryPubSub()
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("a_chan", "hello universe!")
    assert subscriber.messages.qsize() == 2, subscriber.messages.qsize()
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_subscribe_multiple_chan():
    pubsub = MemoryPubSub()
    subscriber = await pubsub.subscribe("a_chan", "b_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("b_chan", "hello universe!")
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_not_subscribed_chan():
    pubsub = MemoryPubSub()
    subscriber = await pubsub.subscribe("a_chan", "c_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("b_chan", "junk message")
    await pubsub.publish("c_chan", "hello universe!")
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_dispose_subscriber():
    pubsub = MemoryPubSub()
    subscriber = await pubsub.subscribe("a_chan")
    assert await pubsub.publish("a_chan", "hello world!") == 1
    del subscriber
    assert await pubsub.publish("a_chan", "hello world!") == 0
