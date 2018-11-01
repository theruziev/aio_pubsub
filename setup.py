from setuptools import setup, find_packages
import sys
import os

py_version = sys.version_info[:2]

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

setup(
    name='async_pubsub',
    version='0.1',
    description="A generic interface wrapping multiple backends to provide a consistent pubsub API.",
    long_description=README,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='pubsub pub/sub redis mongodb',
    author='Bakhtiyor Ruziev',
    author_email='bakhtiyor.ruziev@yandex.ru',
    url='http://github.com/bruziev/async_pubsub',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'redis': [
            'redis > 2.10',
        ],
        'mongodb': [
            'motor >= 2',
        ],
        'amqp': [
            'amqp >= 1.4.9'
        ]
    },

)
