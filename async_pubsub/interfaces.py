import typing
from abc import ABCMeta, abstractmethod


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
    async def publish(self, channel: typing.Any, message: typing.Any):
        """Publish a message to channel"""

    @abstractmethod
    async def subscribe(self, channel: typing.Any):
        """Subscribe to one or many channels and return a Subscriber object"""
