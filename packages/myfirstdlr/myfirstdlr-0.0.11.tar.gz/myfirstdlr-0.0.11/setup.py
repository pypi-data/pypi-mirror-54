#!/usr/bin/env python
# coding: utf-8

import setuptools

setuptools.setup(
  name='myfirstdlr',
  version='0.0.11',
  author='whoami',
  author_email='wai@yy.com',
  description=u'testing...',
  packages=setuptools.find_packages(),
  url='https://google.com',
  entry_points={
    'console_scripts': [
      'foo=myfirstdlr.spt:foo'
    ]
  }
)
