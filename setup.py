from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# parse description from README.md
try:
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        readme_header = f.read().split('\n', 2)
        short_description = readme_header[0].split(': ')[-1] + '.'
        long_description = readme_header[2].split('\n', 2)[2].split('\n\n')[0].replace('\n', ' ').replace('`', '')
except Exception:
    print('[!] Failed to parse package description from README.md')
    short_description = 'A library for storing huge integeters efficiently'
    long_description = 'This python library helps store massive integers by using a gzipped-string representation in memory.'

setup(
    name='gzint',
    version='0.0.4',
    description=short_description,      # parsed from first line of README.md
    long_description=long_description,  # parsed from first section of README.md

    url='https://github.com/pirate/gzint',
    author='Nick Sweeting',
    author_email='gzint@sweeting.me',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3 :: Only',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],
    keywords='int bigint integers memory gzip storage compression math',

    packages=['gzint'],
    test_suite='gzint.tests',
    install_requires=[],
)
