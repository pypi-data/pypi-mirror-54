# coding: utf-8

from setuptools import setup

setup(
    name='pyplurky',
    version='0.2.3',
    author='Dephilia',
    author_email='leedaniel682@gmail.com',
    url='https://github.com/Dephilia/PyPlurky',
    description=u'A plurk-bot pack with plurk-api wrapper written in Python.',
    packages=['pyplurky'],
    install_requires=[
    'schedule'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # entry_points={
    #     'console_scripts': [
    #         '<cmd>=<file>:<func>'
    #     ]
    # }
)
