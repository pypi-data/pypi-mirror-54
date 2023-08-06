# coding: utf-8
from setuptools import setup

with open('README.rst') as f:
    long_description = f.read()

setupargs = {
    'name': 'myorm',
    'description': 'Provides a simple ORM for MySQL, PostgreSQL and SQLite.',

    'license': 'GPLv3',
    'version': '0.5.0',

    'packages': ['myorm', 'myorm.adaptors'],
    'long_description': long_description,
    'long_description_content_type': 'text/x-rst',

    'author': 'Christian Kokoska',
    'author_email': 'christian@eternalconcert.de',
    'install_requires': [],
}

if __name__ == '__main__':
    setup(**setupargs)
