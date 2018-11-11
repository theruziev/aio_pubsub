AsyncPubSub
===========

.. image:: https://travis-ci.com/bruziev/async_pubsub.svg?branch=master
   :target: https://travis-ci.com/bruziev/async_pubsub

.. image:: https://codecov.io/gh/bruziev/async_pubsub/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bruziev/async_pubsub/branch/master


A generic interface wrapping multiple backends to provide a consistent pubsub API.


Usage
------
To use, you need to implement your pubsub implementation from interfaces or use backends
from ``async_pubsub.backends`` package::

    from async_pubsub.backends.memory import MemoryPubSub
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

``Disclaimer``: I would not advise you to use this backends, 'cause they are shown only for testing
or for develop yours:

* memory
* mongodb