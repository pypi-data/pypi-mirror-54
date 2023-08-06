#!/usr/bin/env python3
# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
# LICENSE: Distributed under the terms of the MIT License
#

longdesc = '''
This is a library for connecting to the Hologram Cloud
'''

import sys
try:
    from setuptools import setup, find_packages
    kw = {
    }
except ImportError:
    from distutils.core import setup
    kw = {}

if sys.platform == 'darwin':
    import setup_helper
    setup_helper.install_custom_make_tarball()

setup(
    name = 'hologram-python',
    version = open('version.txt').read().split()[0],
    description = 'Library for accessing Hologram Cloud at https://hologram.io',
    long_description = longdesc,
    author = 'Hologram',
    author_email = 'support@hologram.io',
    url = 'https://github.com/hologram-io/hologram-python/',
    packages = find_packages(),
    include_package_data = True,
    install_requires = open('requirements.txt').read().split(),
    scripts = ['scripts/hologram'],
    license = 'MIT',
    platforms = 'Posix; MacOS X; Windows',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
    **kw
)
