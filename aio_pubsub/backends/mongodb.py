import asyncio
import time
from datetime import datetime

from aio_pubsub.interfaces import PubSub, Subscriber
from aio_pubsub.typings import Message

motor_installed = False
try:
    import motor.motor_asyncio
    import pymongo

    motor_installed = True
except ImportError:  # pragma: no cover
    pass


class MongoDBSubscriber(Subscriber):
    def __init__(self, channel, collection):
        self.channel = channel
        self.collection = collection
        self.now = datetime.utcnow()
        self.cursor = self.collection.find(
            {"channel": self.channel, "when": {"$gte": self.now}},
            cursor_type=pymongo.CursorType.TAILABLE_AWAIT,
        )

    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            while self.cursor.alive:  # pragma: no cover
                try:
                    async for message in self.cursor:
                        if "message" in message and message["message"] is not None:
                            return message["message"]
                except StopIteration:  # pragma: no cover
                    pass
            self.cursor = self.collection.find(
                {"channel": self.channel, "when": {"$gte": self.now}},
                cursor_type=pymongo.CursorType.TAILABLE_AWAIT,
            )
            await asyncio.sleep(1)


class MongoDBPubSub(PubSub):
    def __init__(self, collection):
        self._collection = collection

    async def publish(self, channel: str, message: Message):
        await self._collection.insert_one({"channel": channel, "message": message, "when": datetime.utcnow()})

    async def subscribe(self, channel) -> "MongoDBSubscriber":
        return MongoDBSubscriber(channel, self._collection)

    @staticmethod
    async def get_collection(
        host=None,
        port=None,
        max_pool_size=100,
        database="aio_pubsub",
        collection="aio_pubsub_messages",
        collection_size=10 * 2 ** 20,
    ):
        if motor_installed is False:
            raise RuntimeError("Please install `motor`")  # pragma: no cover
        client = motor.motor_asyncio.AsyncIOMotorClient(host=host, port=port, maxPoolSize=max_pool_size)

        db = client[database]

        try:
            await db.create_collection(collection, size=collection_size, capped=True)
        except pymongo.errors.CollectionInvalid:
            pass
        collection = db[collection]

        return collection
