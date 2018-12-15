import asyncio
import logging
from datetime import datetime
from aio_pubsub.interfaces import PubSub, Subscriber

motor_installed = False
try:
    from pymongo.errors import CollectionInvalid
    from pymongo import CursorType
    import motor.motor_asyncio

    motor_installed = True
except ImportError:
    pass  # pragma: no cover


class MongoSubscriber(Subscriber):
    def __init__(self, collection, channel):

        self.cursor = None
        self.collection = collection
        self.channel = channel
        self.cursor = self.collection.find(
            {"channel": self.channel, "when": {"$gte": datetime.utcnow()}},
            cursor_type=CursorType.TAILABLE_AWAIT,
        )

    def __aiter__(self):
        return self

    async def __anext__(self):
        while self.cursor.alive:
            try:
                async for message in self.cursor:
                    if message["type"] == "message":
                        return message["message"]
            except StopAsyncIteration:
                await asyncio.sleep(0.5)


class MongoPubSub(PubSub):
    def __init__(
        self,
        host="localhost",
        port=27017,
        max_pool_size=100,
        database="anypubsub",
        collection_name="anyps_messages",
        collection_size=10 * 2 ** 20,
    ):
        if motor_installed is False:
            raise RuntimeError("Please install `motor`")  # pragma: no cover
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            host=host, port=port, maxPoolSize=max_pool_size
        )

        self.db = self.client[database]
        self.collection = None
        self.collection_name = collection_name
        self.collection_size = collection_size

    async def init(self):
        try:
            await self.db.create_collection(
                self.collection_name, size=self.collection_size, capped=True
            )
        except CollectionInvalid as e:
            logging.error("Error during create collection: {}".format(e))
        self.collection = self.db[self.collection_name]

    async def publish(self, channel, message):
        await self.collection.insert_one(
            {"type": "message", "channel": channel, "message": message, "when": datetime.utcnow()}
        )

    async def subscribe(self, channel):
        subscriber = MongoSubscriber(self.collection, channel)
        return subscriber
