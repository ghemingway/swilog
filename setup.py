#!/usr/bin/python
# Copyright (c) 2012 G. Hemingway
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
from swilog import __version__ as version

name = 'swilog'

setup(
    name = name,
    version = version,
    description = 'Swilog',
    license = 'Apache License (2.0)',
    author = 'G. Hemingway',
    author_email = 'graham.hemingway@gmail.com',
    url = 'https://github.com/ghemingway/swilog',
    packages = find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Environment :: No Input/Output (Daemon)',
        ],
    keywords = ('backup', 'archive', 'atom', 'rss', 'blog', 'weblog'),
    scripts=['bin/swift-log-uploader.py'],
    data_files=[('/etc/swilog', ['etc/swilog.conf.sample'])],
    install_requires = ['python-swiftclient']
)
