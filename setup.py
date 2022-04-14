#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['requests', 'python-dotenv', 'deprecation', 'protobuf', 'grpcio', 'google-api-python-client']

# removed in 0.7.1 test_requirements = ['pytest']

setup(
    author='Modzy',
    author_email='support@modzy.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description="Modzy's Python SDK queries models, submits inference jobs and returns results directly to your editor.",
    python_requires='>=3.6',
    install_requires=requirements,
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='modzy, sdk',
    name='modzy-sdk',
    packages=find_packages(),
    # removed in 0.7.1 test_suite='tests',
    # removed in 0.7.1 tests_require=test_requirements,
    url='https://github.com/modzy/sdk-python',
    version='0.7.1',
    zip_safe=False,
)
