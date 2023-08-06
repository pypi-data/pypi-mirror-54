#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
  name='myfirstdlr',
  version='0.0.10',
  author='whoami',
  author_email='wai@yy.com',
  description=u'testing...',
  url='https://google.com',
  entry_points={
    'console_scripts': [
      'foo=myfirstdlr.spt:foo'
    ]
  }
)
