# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(
    name='pursue',
    version='0.1.0',
    description='OpenStack Object Storage Python Client featuring client-side object encryption',
    long_description=long_description,
    author='Jaime Gil de Sagredo Luna',
    author_email='jaimegildesagredo@gmail.com',
    packages=find_packages(exclude=['tests', 'tests.*']),
    entry_points={
        'console_scripts': [
            'pursue = pursue.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
