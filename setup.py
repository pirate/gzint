from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# parse description from README.md
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    try:
        readme_header = f.read().split('\n', 2)
        short_description = readme_header[0].split('gzint: ')[-1] + '.'
        long_description = readme_header[2].split('\n', 2)[2].split('\n\n')[0].replace('\n', ' ').replace('`', '')
    except Exception:
        raise ValueError('Failed to parse gzint description from README.md')

setup(
    name='gzint',
    version='0.0.1',
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
    install_requires=[],
    extras_require={
        'dev': ['bpython', 'ipdb'],
    },
)
