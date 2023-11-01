#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import List
from pathlib import Path
from setuptools import setup, find_packages


def requirements(name: str) -> List[str]:
    root = Path(__file__).parent / 'requirements'
    return root.joinpath(name).read_text().splitlines()


with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()


with open('src/bluemoss/__init__.py', encoding='utf-8') as f:
    match = re.search(
        r"^__version__\s=\s'([\d\.]+(?:-[a-zA-Z]+(?:\.\d+)?)?)'$",
        f.read(),
        re.MULTILINE,
    )
    if not match:
        raise RuntimeError('version is not set')

    version = match.group(1)

if not version:
    raise RuntimeError('version is not set')


setup(
    name='bluemoss',
    version=version,
    author='Luca Tabone',
    author_email='luca@tabone.io',
    maintainer='Luca Tabone',
    license='APACHE',
    url='https://github.com/LucaTabone/bluemoss',
    description='bluemoss enables you to easily scrape websites.',
    install_requires=requirements('base.txt'),
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=find_packages(
        where='src',
        include=['bluemoss', 'bluemoss.*'],
    ),
    package_dir={'': 'src'},
    python_requires='>=3.9.0',
    package_data={'': []},
    include_package_data=True,
    zip_safe=False,
    extras_require={},
    entry_points={
        'console_scripts': [],
        'bluemoss': [],
    },
    project_urls={
        'Documentation': 'https://github.com/LucaTabone/bluemoss/blob/main/README.md',
        'Source': 'https://github.com/LucaTabone/bluemoss',
        'Tracker': 'https://github.com/LucaTabone/bluemoss/issues',
    },
    keywords=[
        'xpath',
        'scrape',
        'scraping',
        'bluemoss',
        'webscraping',
        'web-scraping',
        'recipe-scraping',
        'template-scraping',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Typing :: Typed',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Text Processing :: Markup :: XML',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
    ],
)
