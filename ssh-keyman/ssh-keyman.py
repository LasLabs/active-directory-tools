# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.html)

import argparse
import ConfigParser
import logging
import os
from getpass import getpass

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[logging.StreamHandler()]
)

try:
    import ldap
except ImportError:
    logging.error('To use this script, you need to install `python-ldap`')
    exit(0)

parser = argparse.ArgumentParser()
parser.add_argument(
    '--clear', action='store_true', help='Clear the config file before running'
)
args = parser.parse_args()


CONFIG_FILE = '%s/.ssh-keyman' % os.path.expanduser('~')
CONFIG = ConfigParser.ConfigParser()
CREATE_CONFIG = False
if os.path.exists(CONFIG_FILE):
    if args.clear:
        CREATE_CONFIG = True
    else:
        CONFIG.read(CONFIG_FILE)
        for k in ('URI', 'BASE_DN', 'SSH_KEY_ATTR'):
            if not CONFIG.get('ADDC', k):
                CREATE_CONFIG = True
else:
    CREATE_CONFIG = True

if CREATE_CONFIG:
    with open(CONFIG_FILE, 'w') as fh:
        CONFIG.add_section('ADDC')
        server = raw_input('LDAP Server URI: ')
        base_dn = raw_input('Base DN: ')
        ssh_key_attr = raw_input('SSH Key Attribute Name: ')
        CONFIG.set('ADDC','URI', server)
        CONFIG.set('ADDC','BASE_DN', base_dn)
        CONFIG.set('ADDC','SSH_KEY_ATTR', ssh_key_attr)
        CONFIG.set('ADDC','LDAP_SERVER', 'ldap://'+server+':389')
        CONFIG.write(fh)

SSH_KEY_ATTR = CONFIG.get('ADDC','SSH_KEY_ATTR')

try:
    ldap.set_option(ldap.OPT_REFERRALS, 0)
    ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
    ldap.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
    ldap.set_option(ldap.OPT_X_TLS_DEMAND, True)
    ldap_client = ldap.initialize(CONFIG.get('ADDC','LDAP_SERVER'))
    username = raw_input('Username: ')
    password = getpass('Password: ')
    ldap_client.start_tls_s()
    ldap_client.simple_bind_s(username, password)
except ldap.LDAPError as e:
    logging.error(e)
    exit(0)

ldap_filter = 'sAMAccountName=%s' % username.split('@')[0]
user = ldap_client.search_s(
    CONFIG.get('ADDC','BASE_DN'), ldap.SCOPE_SUBTREE,
    ldap_filter, [SSH_KEY_ATTR]
)

user_dn = user[0][0]
keys = user[0][1].get(SSH_KEY_ATTR, [])
host = raw_input('SSH Key Host (or * for global): ')
key = raw_input('SSH Public Key: ')

# Search for any existing SSH keys for this host and remove them
for k in keys:
    if host in key:
        keys.pop(k)

keys.append('%s:%s' % (host, key))

# Replace the SSH_KEY_ATTR
try:
    ldap_client.modify_s(user_dn, [(ldap.MOD_REPLACE, SSH_KEY_ATTR, keys)])
except ldap.LDAPError as e:
    logging.error(e)
    exit(0)
