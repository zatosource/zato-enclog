# -*- coding: utf-8 -*-

"""
Copyright (C) 2018, Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

# Part of Zato - Open-source ESB, SOA, REST, APIs and Cloud Integrations in Python
# https://zato.io

from zato.enclog._core import cli_main, EncryptedLogFormatter, genkey

# For flake8
cli_main
EncryptedLogFormatter
genkey

__import__('pkg_resources').declare_namespace('zato')
