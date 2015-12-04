# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

"""
Copyright (C) 2015 Dariusz Suchojad <dsuch at zato.io>

Licensed under BSD, see LICENSE.txt for terms and conditions.
"""

# Part of Zato - Open-source ESB, SOA, REST, APIs and Cloud Integrations in Python
# https://zato.io

# stdlib
import logging
from unittest import TestCase
from uuid import uuid4

# cryptography
from cryptography.fernet import Fernet

# Zato
from zato.enclog import EncryptedLogFormatter, genkey

class CryptoTestCase(TestCase):
    def test_genkey(self):
        key = genkey()
        Fernet(key) # Must not raise an exception otherwise we've generated an invalid key

    def test_crypto_round_trip(self):
        clear_text = uuid4().hex
        key = genkey()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(clear_text)
        decrypted = fernet.decrypt(encrypted)

        self.assertEquals(clear_text, decrypted)

class FormatterTestCase(TestCase):
    def test_formatter(self):

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
