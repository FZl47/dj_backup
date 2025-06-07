import warnings

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
    IMPORT_STATUS = package_imported
    CONFIG = {
        'BOT_TOKEN': None,
        'CHAT_ID': None,
    }
    STORAGE_NAME = 'TELEGRAM_BOT'
    _BOT = None

    @classmethod
    def _connect(cls):
        """
            create connection to telegram bot
        """
        c = cls.CONFIG
        if not cls._BOT:
            cls._BOT = Bot(token=c['BOT_TOKEN'])
        return cls._BOT

    @classmethod
    def _close(cls):
        cls._BOT = None

    def _upload(self):
        c = self.CONFIG
        with open(self.file_path, 'rb') as f:
            self._BOT.send_document(chat_id=c['CHAT_ID'], document=f)

    def _save(self):
        self.check_before_save()
        self.connect()
        self.upload()
        self.close()
