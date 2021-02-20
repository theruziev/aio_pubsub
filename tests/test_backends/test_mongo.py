import motor
import pytest

from aio_pubsub.backends.mongodb import MongoDBPubSub


@pytest.mark.asyncio
async def test_subscriber_isinstance():
    from aio_pubsub.backends.mongodb import MongoDBSubscriber

    pubsub = MongoDBPubSub(host="localhost", port=27017)
    subscriber = await pubsub.subscribe("a_chan")
    assert isinstance(subscriber, MongoDBSubscriber)


@pytest.mark.asyncio
async def test_iteration_protocol():
    pubsub = MongoDBPubSub(host="localhost", port=27017)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"


@pytest.mark.asyncio
async def test_pubsub():
    pubsub = MongoDBPubSub(host="localhost", port=27017)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("a_chan", "hello universe!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_not_subscribed_chan():
    pubsub = MongoDBPubSub(host="localhost", port=27017)
    subscriber_a_chan = await pubsub.subscribe("a_chan")
    subscriber_c_chan = await pubsub.subscribe("c_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("b_chan", "junk message")
    await pubsub.publish("c_chan", "hello universe!")
    subscriber_a_chan = subscriber_a_chan.__aiter__()
    subscriber_c_chan = subscriber_c_chan.__aiter__()
    assert await subscriber_a_chan.__anext__() == "hello world!"
    assert await subscriber_c_chan.__anext__() == "hello universe!"
