# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


setup(
    name='standup-desktop',
    description='Desktop for standups',
    version='0.0.1.dev0',
    url='https://github.com/waawal/standup-desktop',
    author='Jacek Mitręga',
    license='Apache License, Version 2.0',
    install_requires=open('requirements.txt').read(),
    packages=find_packages(),
    zip_safe=True,
)
