import aiopg
import pytest

from aio_pubsub.backends.postgresql import PostgreSQLPubSub, PostgreSQLSubscriber


@pytest.fixture()
async def pg_pool():
    pool = await aiopg.create_pool(
        "dbname=aiopg user=aiopg password=example host=127.0.0.1 port=5432"
    )
    yield pool
    pool.terminate()


@pytest.mark.asyncio
async def test_init(pg_pool):
    pubsub = PostgreSQLPubSub(pg_pool)
    async with pg_pool.acquire() as pool:
        async with pool.cursor() as cursor:
            await cursor.execute("drop table if exists {};".format(pubsub.table_name))

    await pubsub.init()

    async with pg_pool.acquire() as pool:
        async with pool.cursor() as cursor:
            await cursor.execute("select * from {};".format(pubsub.table_name))
    subscriber = await pubsub.subscribe("a_chan")
    assert isinstance(subscriber, PostgreSQLSubscriber)


@pytest.mark.asyncio
async def test_subscriber_isinstance(pg_pool):
    pubsub = PostgreSQLPubSub(pg_pool)
    await pubsub.init()
    subscriber = await pubsub.subscribe("a_chan")
    assert isinstance(subscriber, PostgreSQLSubscriber)


@pytest.mark.asyncio
async def test_iteration_protocol(pg_pool):
    pubsub = PostgreSQLPubSub(pg_pool)
    await pubsub.init()
    msgs = ["hello world!"]
    for m in msgs:
        await pubsub.publish("a_chan", m)

    res_msgs = []
    async for msg in await pubsub.subscribe("a_chan"):
        res_msgs.append(msg)
    assert msgs == res_msgs


@pytest.mark.asyncio
async def test_pubsub(pg_pool):
    pubsub = PostgreSQLPubSub(pg_pool)
    await pubsub.init()
    msgs = ["hello world!", "hello universe!"]
    for m in msgs:
        await pubsub.publish("a_chan", m)

    res_msgs = []
    for _ in msgs:
        async for msg in await pubsub.subscribe("a_chan"):
            res_msgs.append(msg)

    assert msgs == res_msgs


@pytest.mark.asyncio
async def test_not_subscribed_chan(pg_pool):
    pubsub = PostgreSQLPubSub(pg_pool)
    await pubsub.init()
    msgs = ["hello world!", "hello universe!"]
    msgs_chan_c = ["hello world!", "hello universe!"]
    for m in msgs:
        await pubsub.publish("a_chan", m)
    for m in msgs_chan_c:
        await pubsub.publish("c_chan", m)

    res_msgs = []
    for _ in msgs:
        async for msg in await pubsub.subscribe("a_chan"):
            res_msgs.append(msg)

    assert msgs == res_msgs
