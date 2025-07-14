import warnings
import inspect

from asgiref.sync import async_to_sync

from typing import Optional, Dict, Any

try:
    from telegram import Bot

    package_imported = True
except ImportError:
    package_imported = False
    warnings.warn("""
        To use the storage provider 'Telegram Bot', you need to install its package; otherwise, it cannot be used.
        You can install the required package using the following command:
        'pip install djbackup[telegram]'""")

from .base import BaseStorageConnector


class TelegramBOTConnector(BaseStorageConnector):
    """
        A connector class for interacting with the Telegram Bot API.

        This class provides methods to connect to a Telegram bot and upload files to a specified chat.

        Attributes:
            IMPORT_STATUS (bool): Indicates whether the Telegram package was imported successfully.
            CONFIG (dict): Configuration settings for Telegram bot integration.
            STORAGE_NAME (str): Name of the storage provider.
            _BOT (Optional[Bot]): The Telegram Bot instance.
    """

    IMPORT_STATUS: bool = package_imported
    CONFIG: Dict[str, Optional[Any]] = {
        'BOT_TOKEN': None,
        'CHAT_ID': None,
    }
    STORAGE_NAME = 'TELEGRAM_BOT'
    _BOT: Optional[Bot] = None

    @classmethod
    def _connect(cls) -> Bot:
        """
            Create a connection to the Telegram bot.

            :return: The Bot instance.
        """
        c = cls.CONFIG
        if not cls._BOT:
            cls._BOT = Bot(token=c['BOT_TOKEN'])
        return cls._BOT

    @classmethod
    def _close(cls) -> None:
        """
            Close the connection to the Telegram bot.

            This method sets the bot instance to None, effectively closing the connection.
        """
        cls._BOT = None

    def _upload(self) -> None:
        """
            Upload a file to the specified Telegram chat.

            This method opens the file in binary mode and sends it to the chat defined in the configuration.
        """
        c = self.CONFIG
        with open(self.file_path, 'rb') as f:
            if inspect.iscoroutinefunction(self._BOT.send_document):
                async_to_sync(self._BOT.send_document)(chat_id=c['CHAT_ID'], document=f)
            else:
                self._BOT.send_document(chat_id=c['CHAT_ID'], document=f)

    def _save(self) -> None:
        """
            Save the file to the Telegram bot after performing necessary checks.

            This method checks conditions before saving, establishes a connection,
            uploads the file, and then closes the connection.
        """
        self.check_before_save()
        self.connect()
        self.upload()
        self.close()
