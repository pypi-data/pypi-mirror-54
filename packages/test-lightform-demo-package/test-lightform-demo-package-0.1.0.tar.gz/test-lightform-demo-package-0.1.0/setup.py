
import os
import re
from setuptools import find_packages, setup


def get_version():

    ver_file = 'test_lightform_demo_package/_version.py'
    with open(ver_file) as handle:
        ver_str_line = handle.read()

    ver_pattern = r'^__version__ = [\'"]([^\'"]*)[\'"]'
    match = re.search(ver_pattern, ver_str_line, re.M)
    if match:
        ver_str = match.group(1)
    else:
        msg = 'Unable to find version string in "{}"'.format(ver_file)
        raise RuntimeError(msg)

    return ver_str


setup(
    name='test-lightform-demo-package',
    version=get_version(),
    description='This package does some very useful things.',
    author='Adam J. Plowman',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    project_urls={
        'Github': 'https://github.com/aplowman/test-lightform-demo-package',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
    ],
)
