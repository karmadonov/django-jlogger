#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils import setup

setup(
      name='django-jlogger',
      version='0.0.1',
      description='Simple logging to a database for Django',
      author='Kirill Karmadonov',
      author_email='kirill@live.com',
      url='https://github.com/0xKirill/django-jlogger',
      packages=['jlogger', 'jlogger.management'],
)
