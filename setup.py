from setuptools import setup, find_packages
import os

# Define version in one place
VERSION = "0.1.9"

# Read the contents of README.markdown file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.markdown'), encoding='utf-8') as f:
    long_description = f.read()

# Get the data files
with open(os.path.join(this_directory, "datafiles.txt"), "r") as file:
    data_files = [line.rstrip() for line in file]
    
setup(
    name="sentidict",
    version=VERSION,
    author="Andy Reagan",
    author_email="andy@andyreagan.com",
    description="Utilities for dictionary-based sentiment analysis. Includes 28 sentiment dictionaries with loaders, scoring, and interactive visualization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andyreagan/sentidict",
    project_urls={
        "Bug Tracker": "https://github.com/andyreagan/sentidict/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    package_data={"sentidict": ["static/*","templates/*"] + data_files},
    python_requires=">=3.9",
    install_requires=[
        "marisa_trie",
        "numpy",
        "jinja2",
    ],
    extras_require={
        "dev": ["ipython", "twine", "Sphinx", "recommonmark"],
        "test": ["nose2", "cov-core", "scipy", "jupyter"],
    },
    keywords="sentiment emotion nlp text-analysis",
)
