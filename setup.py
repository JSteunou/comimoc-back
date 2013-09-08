#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pip.req import parse_requirements
from setuptools import setup, find_packages


setup(name='comimoc',
      version='1.0.0',
      description='Comimoc backend for Comimoc project',
      author='Jérôme Steunou',
      author_email='contact@jeromesteunou.net',
      packages=find_packages(),
      include_package_data=True,
      url='https://github.com/JSteunou/comimoc-back',
      install_requires=[str(r.req) for r in parse_requirements('requirements.txt')]
     )
