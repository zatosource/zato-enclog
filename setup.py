# -*- coding: utf-8 -*-

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Originally part of Zato - open-source ESB, SOA, REST, APIs and cloud integrations in Python
# https://zato.io

from __future__ import absolute_import, division, print_function, unicode_literals

import os, sys
from setuptools import setup, find_packages

version = '1.0.5.post2'

LONG_DESCRIPTION = """

===========
zato-enclog
===========

* Encrypted logger which stores everything using Fernet keys (AES128). Safe to use in environments
  that cannot store Personally Identifiable Information (PII) in clear text, such as HIPAA-compliant applications.

* Comes with a command line tool that is used to decrypt logs, including both open and tail -f functionality.

* Learn more about Fernet: https://cryptography.io/en/latest/fernet/

::

  # stdlib
  import logging

  # Zato
  from zato.enclog import EncryptedLogFormatter, genkey

  level = logging.INFO
  format = '%(levelname)s - %(message)s'

  key = genkey()
  formatter = EncryptedLogFormatter(key, format)

  handler = logging.StreamHandler()
  handler.setFormatter(formatter)

  logger = logging.getLogger('')
  logger.addHandler(handler)
  logger.setLevel(level)

  logger.info(b'{"user":"Jane Xi"}')

  # Shows the following
  INFO - gAAAAABWYa17oiDoSMVjF8JM9DWzB3dtEvenW9laKqgsFl4d4ksbLCkoJzTyrI3nXKYVOcC03dhJ_BwfWlBN3CdGxJZAwMmfUbUzLHkqw2JeTzdgtz0YEGU=
"""

def parse_requirements(requirements):
    with open(requirements) as f:
        return [line.strip('\n') for line in f if line.strip('\n') and not line[0] in ('#',)]

package_dir = b'src' if sys.version_info.major == 2 else 'src'

setup(
      name = 'zato-enclog',
      version = version,

      scripts = ['src/zato/enclog/console/enclog'],

      author = 'Dariusz Suchojad',
      author_email = 'dsuch at zato.io',
      url = 'https://zato.io/docs/progguide/enclog/index.html',
      description = 'Encrypted logger reusable in any Python application',
      long_description = LONG_DESCRIPTION,
      platforms = ['OS Independent'],
      license = 'BSD License',

      package_dir = {'':package_dir},
      packages = find_packages(package_dir),

      namespace_packages = ['zato'],
      install_requires = parse_requirements(
          os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')),

      zip_safe = False,

      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Education :: Testing',
        'Topic :: Internet',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Security',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
        ],
)
