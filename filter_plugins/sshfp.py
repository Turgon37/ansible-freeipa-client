# Copyright (c) 2017 Pierre-GINDRAUD
# The MIT License (MIT)


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError

import base64
import hashlib


# Mapping between SSH Key type in raw SSH strings
g_type_mapping = dict({
    'ssh-rsa': 1,
    'rsa': 1,
    'dsa': 2,
    'ssh-dss': 2,
    'ssh-ecdsa': 3,
    'ecdsa-sha2-nistp256': 3,
    'ssh-ed25519': 4,
    'ed25519': 4
})

# Mapping of fingerprint digests
g_digest_mapping = dict({
    'SHA-1': 1,
    'SHA1': 1,
    'SHA-256': 2,
    'SHA256': 2
})

"""
This filter takes in input SSH public keys in raw format and produce SSHFP entries ready to be put in a dns zone
"""


def sshfp_from_string(value, fingerprint_type='SHA-1'):
    """Build a SSFP entry from a raw ssh key string

    @param string value : the raw ssh public key as ssh-keygen can produce
         Ex: ssh-rsa EFZFZEZFZFZFZEFZE....
    @param string|int fingerprint_type : the type of fingerprint to produce, see g_digest_mapping above
    """
    if not isinstance(value, (str, unicode)):
        raise AnsibleFilterError('A string was expected')
    parts = value.split()
    if len(parts) != 2:
        raise AnsibleFilterError("Expected string composed of two parts TYPE and KEY, given string contains only '{}'".format(len(parts)))
    return sshfp_from_key(parts[0], parts[1], fingerprint_type)

def sshfp_from_key(type, key, fingerprint_type='SHA-1'):
    """Build a SSFP entry from parts of a ssh key 

    @param string type : the type part of the ssh public key, see g_type_mapping above
         Ex: ssh-rsa
    @param string key : the key part of the ssh public key
    @param string|int fingerprint_type : the type of fingerprint to produce, see g_digest_mapping above
    """
    if not type in g_type_mapping:
        raise AnsibleFilterError("The given SSH key type '{}' is unknown".format(type))
    if isinstance(fingerprint_type, str):
        if fingerprint_type in g_digest_mapping:
            digest_type = g_digest_mapping[fingerprint_type]
        else:
            raise AnsibleFilterError("Unknown digest type '{}'. Available {}".format(fingerprint_type, g_digest_mapping.values()))
    elif isinstance(fingerprint_type, int):
        if fingerprint_type in g_digest_mapping.values():
            digest_type = fingerprint_type
        else:
            raise AnsibleFilterError("Unknown digest type '{}'. Available {}".format(fingerprint_type, g_digest_mapping.values()))
    else:
        raise AnsibleFilterError('Bad value for fingerprint_type argument')

    entry = dict({
        'algorythm': g_type_mapping[type],
        'digest_type': digest_type
    })

    try:
        rawkey = base64.b64decode(key)
    except TypeError:
        raise AnsibleFilterError('Failed to base64 decode the given raw key')

    if digest_type == g_digest_mapping['SHA-1']:
        digest_function = hashlib.sha1
    elif digest_type == g_digest_mapping['SHA-256']:
        digest_function = hashlib.sha256
    else:
        raise AnsibleFilterError('Unknown digest type')

    entry['fingerprint'] = digest_function(rawkey).hexdigest().upper()
    return entry

# ---- Ansible filters ----
class FilterModule(object):
    ''' URI filter '''

    def filters(self):
        return {
            'ssh_key_string_to_sshfp': sshfp_from_string
        }
