#!/usr/bin/python

import setuptools

with open("./blocklist_aggregator/__init__.py", "r") as fh:
    for line in fh.read().splitlines():
        if line.startswith('__version__'):
            PKG_VERSION = line.split('"')[1]
if PKG_VERSION.startswith("v"):
    PKG_VERSION = PKG_VERSION[1:]
    
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    
KEYWORDS = ('blocklist aggregator domains dns blacklist whitelist')

setuptools.setup(
    name="blocklist_aggregator",
    version=PKG_VERSION,
    author="Denis MACHARD",
    author_email="d.machard@gmail.com",
    description="Domains blocklist aggregator",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dmachard/blocklist-aggregator",
    packages=['blocklist_aggregator'],
    include_package_data=True,
    platforms='any',
    keywords=KEYWORDS,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=[
        "pyyaml",
        "requests"
    ]
)
