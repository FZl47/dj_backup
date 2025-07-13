from typing import Type

from .base import SecureBaseABC
from .aes import AESEncryption
from .zipp import ZipPassword

_ENCRYPTION_TYPES = {
    'zipp': ZipPassword,
    'aes': AESEncryption
}

EncTypeUnion = Type[SecureBaseABC]


def get_enc_by_name(name: str) -> EncTypeUnion:
    try:
        return _ENCRYPTION_TYPES[name]
    except KeyError:
        raise ValueError(f"Encryption type '{name}' is not supported.")
