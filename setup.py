# from distutils.core import setup
from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name = 'sentidict',
    packages = ['sentidict'],
    package_data={'sentidict': ['static/*','templates/*']},
    version = '0.1',
    description = 'Utilities for dictionary-based sentiment analysis. Includes 28 sentiment dictionaries with loaders, scoring, and interactive visualization.',
    long_description = long_description,
    install_requires=['marisa_trie','numpy','jinja2'],
    extras_require={
        'dev': ['ipython','twine','Sphinx','recommonmark'],
        # http://nose2.readthedocs.io/en/latest/plugins/coverage.html
        'test': ['nose2','cov-core','scipy','jupyter'],
    },
    author = 'Andy Reagan',
    author_email = 'andy@andyreagan.com',
    url = 'https://github.com/andyreagan/sentidict', 
    download_url = 'https://github.com/andyreagan/sentidict/tarball/0.1a',
    keywords = 'sentiment emotion',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',],
    )
