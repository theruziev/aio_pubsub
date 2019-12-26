from setuptools import setup, find_packages
import os
from aio_pubsub._version import __version__

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='aio_pubsub',
    version=__version__,
    description="A generic interface wrapping multiple backends to provide a consistent pubsub API.",
    long_description=README,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='pubsub pub/sub mongodb',
    author='Bakhtiyor Ruziev',
    author_email='bakhtiyor.ruziev@yandex.ru',
    url='http://github.com/bruziev/async_pubsub',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'aioredis': [
            'aioredis >= 1.2.0',
        ],
        'aiopg': [
            'aiopg >= 1.0.0',
        ],

    },

)
