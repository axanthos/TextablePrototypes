#!/usr/bin/env python

""" File setup.py

Copyright 2016 University of Lausanne (aris.xanthos@unil.ch)

This file is part of the Textable Prototypes (v0.1) extension to 
Orange Canvas.

Textable Prototypes v0.1 is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Textable Prototypes v0.1 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Textable Prototypes v0.1. If not, see http://www.gnu.org/licenses
"""

__version__ = "0.1.0"

import os

from setuptools import setup, find_packages

NAME = 'Orange-Textable-Prototypes'
DOCUMENTATION_NAME = 'Orange Textable Prototypes'

VERSION = '0.1.0'

DESCRIPTION = 'Extra widgets for the Orange Textable text analysis package.'
LONG_DESCRIPTION = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
AUTHOR = 'University of Lausanne'
AUTHOR_EMAIL = 'aris.xanthos@unil.ch'
URL = 'https://github.com/axanthos/TextablePrototypes'
DOWNLOAD_URL = 'https://github.com/axanthos/TextablePrototypes/downloads'
LICENSE = 'GPLv3'

KEYWORDS = (
    'text mining',
    'text analysis',
    'textable',
    'orange',
    'orange add-on',
)

CLASSIFIERS = (
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 2 :: only',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing :: General',
    'Topic :: Text Processing :: Linguistic',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
)

PACKAGES = find_packages(
)

PACKAGE_DATA = {
}

INSTALL_REQUIRES = (
    'Orange',
    'Orange-Textable',
    'setuptools',
),

EXTRAS_REQUIRE = {
}

DEPENDENCY_LINKS = (
)

ENTRY_POINTS = {
    'orange.addons': (
        'ttp = _textable_prototypes',
    ),
    'orange.widgets': (
        'Textable-Prototypes = _textable_prototypes.widgets',
    ),
    'orange.canvas.help': (
        'intersphinx = _textable_prototypes:doc_root'
    ),
}

if __name__ == '__main__':
    setup(
        name = NAME,
        version = VERSION,
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        author = AUTHOR,
        author_email = AUTHOR_EMAIL,
        url = URL,
        download_url = DOWNLOAD_URL,
        license = LICENSE,
        keywords = KEYWORDS,
        classifiers = CLASSIFIERS,
        packages = PACKAGES,
        package_data = PACKAGE_DATA,
        install_requires = INSTALL_REQUIRES,
        extras_require = EXTRAS_REQUIRE,
        dependency_links = DEPENDENCY_LINKS,
        entry_points = ENTRY_POINTS,
        include_package_data = True,
        zip_safe = False,
    )


