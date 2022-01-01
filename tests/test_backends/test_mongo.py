import motor
import pytest

from aio_pubsub.backends.mongodb import MongoDBPubSub


@pytest.fixture
async def create_pub_sub_conn():
    collection = await MongoDBPubSub.get_collection(host="localhost", port=27017)
    yield collection


@pytest.mark.asyncio
async def test_subscriber_isinstance(create_pub_sub_conn):
    from aio_pubsub.backends.mongodb import MongoDBSubscriber

    pubsub = MongoDBPubSub(create_pub_sub_conn)
    subscriber = await pubsub.subscribe("a_chan")
    assert isinstance(subscriber, MongoDBSubscriber)


@pytest.mark.asyncio
async def test_iteration_protocol(create_pub_sub_conn):
    pubsub = MongoDBPubSub(create_pub_sub_conn)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"


@pytest.mark.asyncio
async def test_pubsub(create_pub_sub_conn):
    pubsub = MongoDBPubSub(create_pub_sub_conn)
    subscriber = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("a_chan", "hello universe!")
    subscriber = subscriber.__aiter__()
    assert await subscriber.__anext__() == "hello world!"
    assert await subscriber.__anext__() == "hello universe!"


@pytest.mark.asyncio
async def test_not_subscribed_chan(create_pub_sub_conn):
    pubsub = MongoDBPubSub(create_pub_sub_conn)
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
async def test_broadcast(create_pub_sub_conn):
    pubsub = MongoDBPubSub(create_pub_sub_conn)
    subscriber_1 = await pubsub.subscribe("a_chan")
    subscriber_2 = await pubsub.subscribe("a_chan")
    await pubsub.publish("a_chan", "hello world!")
    subscriber_1 = subscriber_1.__aiter__()
    subscriber_2 = subscriber_2.__aiter__()
    assert await subscriber_1.__anext__() == "hello world!"
    assert await subscriber_2.__anext__() == "hello world!"
