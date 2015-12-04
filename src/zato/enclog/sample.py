# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Part of Zato - Open-source ESB, SOA, REST, APIs and Cloud Integrations in Python
# https://zato.io

# stdlib
import logging

# Zato
from enclog import EncryptedLogFormatter, genkey

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
