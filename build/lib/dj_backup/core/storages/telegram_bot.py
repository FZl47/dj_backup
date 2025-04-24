from telegram import Bot

from .base import BaseStorageConnector


class TelegramBOTConnector(BaseStorageConnector):
    CONFIG = {
        'BOT_TOKEN': None,
        'CHAT_ID': 22,
        'TIMEOUT': 60
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
            self._BOT.send_document(chat_id=c['CHAT_ID'], document=f, timeout=c['TIMEOUT'])

    def _save(self):
        self.check_before_save()
        self.connect()
        self.upload()
        self.close()
