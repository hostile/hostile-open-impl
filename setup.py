from setuptools import setup

setup(
    name='hostile_open',
    version='1.0.0',
    packages=['hostile_open'],
    install_requires=[x.strip() for x in open('requirements.txt', 'r').readlines()]
)