from abc import ABC
from pathlib import Path
from typing import Union, Any

from dj_backup.models import DJDataBaseBackUp, DJFileBackUp


class SecureBaseABC(ABC):
    """
        A base class for implementing secure backup mechanisms.

        This class provides an interface for creating secure backup.
        It requires subclasses to implement the encryption and decryption methods,
        ensuring that any backup object can be securely processed.

        Attributes:
            backup_obj (DJDataBaseBackUp | DJFileBackUp):
                The backup object that this class will operate on, which can be
                either a database backup or a file backup.

    """

    def __init__(self, backup_obj: Union[DJDataBaseBackUp, DJFileBackUp]) -> None:
        self.backup_obj = backup_obj

    def save(self, *args, **kwargs) -> Path:
        """
            Must be implemented in subclass.

            get encrypt content and save
        """
        raise NotImplementedError

    def encrypt(self, *args, **kwargs) -> Any:
        """
            Must be implemented in subclass.
        """
        raise NotImplementedError

    def decrypt(self, *args, **kwargs) -> Any:
        """
            Must be implemented in subclass.
        """
        raise NotImplementedError
