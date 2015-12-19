# -*- coding: utf-8 -*-
#
# Copyright 2015 Federico Ficarelli
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

import glob
import os
import sys


if __name__ == "__main__":
    DIRNAME = os.path.abspath(os.path.dirname(__file__))
    if DIRNAME:
        os.chdir(DIRNAME)
    try:
        py_dirname = DIRNAME
        sys.path.insert(0, py_dirname)
    
        import overload
        version = overload.__version__
    finally:
        del sys.path[0]
    
    # search executables
    scripts = []
    for filepath in glob.glob('bin/*'):
        if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
            scripts.append(filepath)
    
    # search packages
    root_packages = []
    packages = []
    for package in root_packages:
        package_dirname = os.path.join(DIRNAME, package)
        for dirpath, dirnames, filenames in os.walk(package_dirname):
            if '__init__.py' in filenames:
                rdirpath = os.path.relpath(dirpath, DIRNAME)
                packages.append(os.path.normpath(rdirpath).replace(os.sep, '.'))

    setup(
        name="python-overload",
        version=version,
        requires=[],
        description="Improved type dispatch decorator for Python.",
        author="Federico Ficarelli",
        author_email="federico.ficarelli@gmail.com",
        install_requires=(),
        package_data={},
        url="https://nazavode.github.io",
        packages=packages,
        scripts=scripts,
        py_modules=['overload'],
        classifiers=[
            # status:
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',
            # audience:
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            # license:
            'License :: OSI Approved :: Apache Software License',
            # language:
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 2.7',
        ],
        keywords='overload singledispatch type dispatch visitor pattern',
    )
