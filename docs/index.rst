.. AsyncSender documentation master file, created by
   sphinx-quickstart on Fri Nov  2 12:53:23 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AioPubsub's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :hidden:

   aio_pubsub


.. image:: https://travis-ci.com/bruziev/async_pubsub.svg?branch=master
   :target: https://travis-ci.com/bruziev/async_pubsub

.. image:: https://codecov.io/gh/bruziev/async_pubsub/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bruziev/async_pubsub/branch/master


A generic interface wrapping multiple backends to provide a consistent pubsub API.


Usage
------
To use it, you need to implement your pubsub implementation from interfaces or use backends
from ``aio_pubsub.backends`` package::

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
* mongodb
* redis