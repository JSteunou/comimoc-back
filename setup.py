#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip.req import parse_requirements
from setuptools import setup, find_packages

from comimoc import __version__

setup(name='comimoc',
      version=__version__,
      description='Comimoc backend for Comimoc',
      long_description=open('README.md').read(),
      author='Jérôme Steunou',
      author_email='contact@jeromesteunou.net',
      package=find_packages(),
      include_package_data=True,
      url='',
      install_requires=[str(r.req) for r in parse_requirements('requirements.txt')]
     )
