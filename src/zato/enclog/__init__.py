# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>

Licensed under BSD, see LICENSE.txt for terms and conditions.
"""

# Part of Zato - Open-source ESB, SOA, REST, APIs and Cloud Integrations in Python
# https://zato.io

from zato.enclog._core import EncryptedLogFormatter, genkey

# For flake8
EncryptedLogFormatter
genkey

__import__('pkg_resources').declare_namespace('zato')
