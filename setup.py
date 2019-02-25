#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glob import glob
from setuptools import setup, find_packages
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession
import re
import ast
import os

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('src/rev_ai/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

parsed_requirements = parse_requirements(
    'requirements.txt',
    session=PipSession())
parsed_test_requirements = parse_requirements(
    'requirements_dev.txt',
    session=PipSession())
requirements = [str(ir.req) for ir in parsed_requirements]
test_requirements = [str(tr.req) for tr in parsed_test_requirements]

setup(
    name='rev_ai',
    version=version,
    description='Rev.ai makes speech applications easy to build!',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    author="Rev Ai",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[os.path.splitext(os.path.basename(path))[0]
                for path in glob('src/*.py')],
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
