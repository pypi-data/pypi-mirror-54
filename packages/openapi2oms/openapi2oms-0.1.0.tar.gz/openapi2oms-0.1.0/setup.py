# -*- coding: utf-8 -*-
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='openapi2oms',
    version='0.1.0',
    author='Storyscript',
    author_email='support@storyscript.io',
    description='A tool to convert an OpenAPI spec to an OMS spec',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/microservices/openapi2oms',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
