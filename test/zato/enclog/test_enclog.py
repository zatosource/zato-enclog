# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

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

# testfixtures
from testfixtures import LogCapture

# Zato
from zato.enclog import EncryptedLogFormatter, genkey
from zato.enclog._core import log_prefix

class CryptoTestCase(TestCase):
    def test_genkey(self):
        key = genkey()
        Fernet(key) # Must not raise an exception otherwise we've generated an invalid key

    def test_crypto_round_trip(self):
        clear_text = uuid4().hex.encode('utf8')
        key = genkey()
        fernet = Fernet(key)
        encrypted = fernet.encrypt(clear_text)
        decrypted = fernet.decrypt(encrypted)

        self.assertEquals(clear_text, decrypted)

class FormatterTestCase(TestCase):

    def test_formatter(self):

            for prefix in ['±±±', 'abc']:

                with LogCapture() as lc:

                    data = '{}{}'.format(prefix, uuid4().hex)
                    key = genkey()
                    fernet = Fernet(key)

                    level = logging.INFO
                    format = '%(levelname)s - %(message)s'
                    formatter = EncryptedLogFormatter(key, format)

                    handler = logging.StreamHandler()
                    handler.setFormatter(formatter)

                    logger = logging.getLogger('')
                    logger.addHandler(handler)
                    logger.setLevel(level)

                    logger.info(data)

                    encrypted = list(lc.records)[0].msg
                    encrypted = encrypted.split(log_prefix)[1]
                    decrypted = fernet.decrypt(encrypted.encode('utf8')).decode('utf8')

                    self.assertEquals(data, decrypted)
