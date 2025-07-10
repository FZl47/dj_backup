from typing import Union

from .base import SecureBaseABC
from .aes import AESEncryption
from .zipp import ZipPassword

_ENCRYPTION_TYPES = {
    'zipp': ZipPassword,
    'aes': AESEncryption
}

EncTypeUnion = Union[tuple(_ENCRYPTION_TYPES.values())]


def get_enc_by_name(name: str) -> EncTypeUnion:
    return _ENCRYPTION_TYPES[name]
