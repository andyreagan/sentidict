from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name = 'sentidict',
    packages = ['sentidict'],
    package_data={'sentidict': ['data/*','static/*',]},
    version = '0.0.3',
    description = 'Basic usage script for dictionary-based sentiment analysis. Includes 24 sentiment dictionaries.',
    long_description = long_description,
    install_requires=['marisa_trie','numpy','jinja2'],
    extras_require={
        'dev': ['ipython,twine'],
        'test': ['nose2'],
    },
    author = 'Andy Reagan',
    author_email = 'andy@andyreagan.com',
    url = 'https://github.com/andyreagan/sentidict', 
    download_url = 'https://github.com/andyreagan/sentidict/tarball/0.1',
    keywords = 'sentiment emotion',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',],
    )





