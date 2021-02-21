AioPubSub
=========

.. image:: https://travis-ci.com/theruziev/aio_pubsub.svg?branch=master
   :target: https://travis-ci.com/theruziev/aio_pubsub

.. image:: https://codecov.io/gh/theruziev/aio_pubsub/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/theruziev/aio_pubsub/branch/master


A generic interface wrapping multiple backends to provide a consistent pubsub API.

Installation
------------

.. code-block:: bash

    pip install aio-pubsub
    # for redis backend
    pip install aio-pubsub[aioredis]
    # for postgresql backend
    pip install aio-pubsub[aiopg]

Usage
------
To use it, you need to implement your pubsub implementation from interfaces or use backends
from ``aio_pubsub.backends`` package

.. code-block:: python

    import asyncio

    from aio_pubsub.backends.memory import MemoryPubSub

    pubsub = MemoryPubSub()


    async def sender():
        """Publish a new message each second"""
        counter = 0
        while True:
            await pubsub.publish("a_chan", "hello world %s !" % counter)

            await asyncio.sleep(1)
            counter += 1


    async def receiver():
        """Print all message received from channel"""

        subscriber = await pubsub.subscribe("a_chan")

        async for message in subscriber:
            print("Received message: '%s'" % message)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(sender(), receiver())
    )
    loop.close()


Supported backends
---------------------

``Disclaimer``: I would not advise you to use this backend, because it is shown only for testing purposes.
Better develop your own implementation.

* memory
* redis
* postgresql
* mongodb