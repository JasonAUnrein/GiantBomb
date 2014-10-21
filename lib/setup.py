#!/usr/bin/env python
'''package setup script.'''
from __future__ import print_function
import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    print("ERROR: This package requires setuptools in order to install.", file=sys.stderr)
    sys.exit(1)


THIS_DIR = os.path.abspath(os.path.dirname(__file__))
PKG_DIR = os.path.join(THIS_DIR, 'lib')
sys.path.append(PKG_DIR)
# Read the version from our project
from giantbomb import __version__

if __name__ == '__main__':
    INSTALL_REQUIRES = ['furl>=0.3.95', 'orderedmultidict>=0.7.3']
    setup(
        name="giantbomb",
        version=__version__,
        description="Download Manager Library",
        author="Jason Unrein",
        url="https://github.com/JasonAUnrein/giantbomb",
        download_url="https://github.com/JasonAUnrein/giantbomb/blob/master/release/giantbomb-{0}.tar.gz".format(__version__),
        install_requires=[],
        packages=find_packages(),
        package_data={"giantbomb": ['.*']},
        zip_safe=True,
        include_package_data=True,
        test_suite="giantbomb.tests",

        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Intended Audience :: Developers',
            'Environment :: Other Environment',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Topic :: Software Development :: Libraries'
        ],

        long_description=open(os.path.join(THIS_DIR, "README.rst"), 'r').read()
    )
