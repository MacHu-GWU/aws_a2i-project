# -*- coding: utf-8 -*-

import hashlib


def sha256_of_bytes(b: bytes) -> str:
    m = hashlib.sha256()
    m.update(b)
    return m.hexdigest()


def vprint(msg: str, verbose: bool):
    if verbose:
        print(msg)
