# -*- coding: utf-8 -*-

from benedict.utils import io_util


def decrypt_with(s, decryptor, encoding='utf-8'):
    b_enc = io_util.decode_base64(s)
    b = decryptor(b_enc)
    s = b.decode(encoding)
    s = s.strip().strip('\x00').strip()
    d = io_util.decode_json(s)
    return d


def encrypt_with(d, encryptor, encoding='utf-8', block_size=None):
    s = io_util.encode_json(d)
    if block_size:
        while len(s) % block_size != 0:
            s += ' '
    b = s.encode(encoding)
    b_enc = encryptor(b)
    s_enc = io_util.encode_base64(b_enc, encoding=encoding)
    return s_enc

