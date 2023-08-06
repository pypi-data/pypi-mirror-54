# coding: utf-8

from setuptools import setup
REQUIRED_PYTHON=(3, 5)
setup(
    name='pyplurky',
    version='0.3.1',
    author='Dephilia',
    author_email='leedaniel682@gmail.com',
    url='https://github.com/Dephilia/PyPlurky',
    description=u'A plurk-bot pack with plurk-api wrapper written in Python.',
    packages=['pyplurky'],
    install_requires=[
    'schedule',
    'plurk-oauth'
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    # entry_points={
    #     'console_scripts': [
    #         '<cmd>=<file>:<func>'
    #     ]
    # }
)
