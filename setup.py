# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="dateparser-pt-br",
    version='0.1',
    author="Anderson Ferraz",
    author_email="amarquesferraz@gmail.com",
    description="A small utility to parse pt_BR dates",
    url="https://github.com/amferraz/dateparser-pt-br",
    packages=['dateparser_ptbr'],
    install_requires=[
            'six==1.7.2',
            'pytz==2013.9',
            'python-dateutil==2.1'
    ],
)
