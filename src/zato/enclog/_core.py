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
import sys
from logging import getLogger, Formatter

# click
import click
click.disable_unicode_literals_warning = True

# cryptography
from cryptography.fernet import Fernet, InvalidToken

# future
from builtins import str

# Tailer
from tailer import follow

# ################################################################################################################################

log_prefix = 'enclogdata:'
log_prefix_len = len(log_prefix)

cli_key_option = '--key'
cli_key_prompt='Crypto key'
cli_key_confirm_prompt=False
cli_key_help='Crypto key to decrypt data with.'

# ################################################################################################################################

class EncryptedLogFormatter(Formatter):
    def __init__(self, key=None, *args, **kwargs):
        key = key or kwargs.pop('fernet_key')
        self.fernet = Fernet(key)
        return super(EncryptedLogFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        msg = record.getMessage()
        if isinstance(msg, str):
            msg = msg.encode('utf8')
        record.msg = '{}{}'.format(log_prefix, self.fernet.encrypt(msg).decode('utf8'))
        return super(EncryptedLogFormatter, self).format(record)

# ################################################################################################################################

def _open(ctx, path, key, needs_tailf=False):
    fernet = Fernet(key)

    # Plain open
    f = open(path)

    # tail -f
    if needs_tailf:
        f = follow(f, delay=0.1)

    for line in f:
        prefix, encrypted = line.split(log_prefix)
        try:
            if isinstance(encrypted, str):
                encrypted = encrypted.encode('utf8')

            sys.stdout.write('{}{}\n'.format(prefix, fernet.decrypt(encrypted).decode('utf8')))
            sys.stdout.flush()
        except InvalidToken:
            sys.stderr.write('Invalid crypto key\n')
            sys.exit(1)

# ################################################################################################################################

@click.group()
def cli_main():
    pass

# ################################################################################################################################

def genkey():
    return Fernet.generate_key()

@click.command()
@click.pass_context
def _genkey(ctx):
    sys.stdout.write('{}\n'.format(genkey()))

@click.command()
@click.pass_context
def demo(ctx):
    plain_text = b'{"user":"Jane Xi"}'
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(plain_text)
    decrypted = fernet.decrypt(encrypted)

    sys.stdout.write('\nPlain text: {}\n'.format(plain_text))
    sys.stdout.write('Key:        {}\n'.format(key))
    sys.stdout.write('Encrypted:  {}\n'.format(encrypted))
    sys.stdout.write('Decrypted:  {}\n\n'.format(decrypted))

def get_arg(name):

    @click.command()
    @click.argument('path', type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
    @click.password_option(cli_key_option, prompt=cli_key_prompt, confirmation_prompt=cli_key_confirm_prompt, help=cli_key_help)
    @click.pass_context
    def _cli_arg(ctx, path, key):
        _open(ctx, path, key.encode('utf-8'), True if name == 'tailf' else False)

    return _cli_arg

cli_main.add_command(_genkey, 'genkey')
cli_main.add_command(demo)

for name in ('open', 'tailf'):
    cli_main.add_command(get_arg(name), name)

# ################################################################################################################################

if __name__ == '__main__':

    level = logging.DEBUG
    format = '%(levelname)s - %(message)s'

    key = Fernet.generate_key()
    formatter = EncryptedLogFormatter(key, format)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = getLogger('')
    logger.addHandler(handler)
    logger.setLevel(level)

    logger.info('{"user":"Jane Xi"')

# ################################################################################################################################
