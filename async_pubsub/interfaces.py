from abc import ABCMeta, abstractmethod


class Subscriber(metaclass=ABCMeta):
    @abstractmethod
    async def __aiter__(self):
        """The subscriber iterable"""


class PubSub(metaclass=ABCMeta):
    @abstractmethod
    async def publish(self, channel, message):
        """Publish a message to channel"""

    @abstractmethod
    async def subscribe(self, *channels):
        """Subscribe to one or many channels and return a Subscriber object"""
