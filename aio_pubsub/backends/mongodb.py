import asyncio
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
        self.cursor = collection.find(
            {"channel": self.channel, "when": {"$gte": datetime.utcnow()}},
            cursor_type=pymongo.CursorType.TAILABLE_AWAIT,
        )

    def __aiter__(self):
        return self

    async def __anext__(self):
        while self.cursor.alive:
            try:
                async for message in self.cursor:
                    return message["message"]
            except StopIteration: # pragma: no cover
                asyncio.sleep(1)


class MongoDBPubSub(PubSub):
    def __init__(
        self,
        host=None,
        port=None,
        maxPoolSize=100,
        database="aio_pubsub",
        collection="aio_pubsub_messages",
        collection_size=10 * 2 ** 20,
    ):
        if motor_installed is False:
            raise RuntimeError("Please install `motor`")  # pragma: no cover

        self._host = host
        self._port = port
        self._maxPoolSize = maxPoolSize

        self._database = database
        self._collection_size = collection_size
        self._collection_name = collection
        self._collection = None

    async def get_collection(self):
        if motor_installed is False:
            raise RuntimeError("Please install `motor`")  # pragma: no cover

        if not self._collection:
            client = motor.motor_asyncio.AsyncIOMotorClient(
                host=self._host, port=self._port, maxPoolSize=self._maxPoolSize
            )

            db = client[self._database]

            try:
                await db.create_collection(
                    self._collection_name, size=self._collection_size, capped=True
                )
            except pymongo.errors.CollectionInvalid:
                pass
            self._collection = db[self._collection_name]

        return self._collection

    async def publish(self, channel: str, message: Message):
        collection = await self.get_collection()
        await collection.insert_one(
            {"channel": channel, "message": message, "when": datetime.utcnow()}
        )

    async def subscribe(self, channel) -> "MongoDBSubscriber":
        collection = await self.get_collection()
        return MongoDBSubscriber(channel, collection)
