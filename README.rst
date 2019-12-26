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

    from aio_pubsub.backends.memory import MemoryPubSub
    pubsub = MemoryPubSub()
    # Create subscriber
    subscriber = await pubsub.subscribe("a_chan")

    # Push message
    await pubsub.publish("a_chan", "hello world!")
    await pubsub.publish("a_chan", "hello universe!")

    # And listening channel
    try:
        async for message in subscriber:
            print(message, flush=True)
    except KeyboardInterrupt:
        print("Finish listening")




Supported backends
---------------------

``Disclaimer``: I would not advise you to use this backend, because it is shown only for testing purposes.
Better develop your own implementation.

* memory
* redis
* postgresql
