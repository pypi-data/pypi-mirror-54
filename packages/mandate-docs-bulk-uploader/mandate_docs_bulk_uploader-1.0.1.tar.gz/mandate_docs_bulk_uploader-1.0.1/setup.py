#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

setup(
    name='mandate_docs_bulk_uploader',
    version='1.0.1',
    description='Mandate docs bulk uploader',
    author='Omar Diaz',
    author_email='omar.diaz@crosslend.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'Click',
      'requests',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'mandate_docs_bulk_uploader=mandate_docs_bulk_uploader:tool',
        ]
    },
)
