from abc import ABCMeta, abstractmethod

from aio_pubsub.typings import Message


class Subscriber(metaclass=ABCMeta):
    """
    Subscriber interface
    """

    @abstractmethod
    def __aiter__(self):
        """The subscriber iterable"""


class PubSub(metaclass=ABCMeta):
    """
    Main interface for implementation
    """

    @abstractmethod
    async def publish(self, channel: str, message: Message):
        """Publish a message to channel"""

    @abstractmethod
    async def subscribe(self, channel: str):
        """Subscribe to one or many channels and return a Subscriber object"""
