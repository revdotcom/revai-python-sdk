#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
from setuptools import setup, find_packages
import re
import ast
import os


def parse_requirements(filehandle):
    for line in filehandle:
        line = line.strip()
        if line == '':
            continue
        # Comments are lines that start with # only.
        elif not line or line.startswith('#'):
            continue
        elif (line.startswith('-r') or line.startswith('--requirement') or
              line.startswith('-f') or line.startswith('--find-links') or
              line.startswith('-i') or line.startswith('--index-url') or
              line.startswith('--extra-index-url') or line.startswith('--no-index') or
              line.startswith('-Z') or line.startswith('--always-unzip')):
            continue
        else:
            yield line


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('src/rev_ai/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt', 'r') as req_file:
    requirements = list(parse_requirements(req_file))

with open('requirements_dev.txt', 'r') as req_dev_file:
    test_requirements = list(parse_requirements(req_dev_file))

setup(
    name='rev_ai',
    version=version,
    description='Rev AI makes speech applications easy to build!',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    author="Rev Ai",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    license='MIT license',
    keywords='rev_ai',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    setup_requires=['pytest-runner==4.2'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/revdotcom/revai-python-sdk',
)
