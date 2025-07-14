import tempfile

from pathlib import Path

from django.test import TestCase

from dj_backup.core.backup.file import FileBackup
from dj_backup.core.utils import delete_item
from dj_backup import models


class FileBackupTest(TestCase):
    _temp_file = None

    def setUp(self):
        # Create File
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            self._temp_file = temp_file
            self.file_obj = models.DJFile.objects.create(
                name='Test File',
                dir=temp_file.name
            )

        # Create FileBackup
        kwargs = {
            'unit': 'minutes',
            'interval': 1,
        }
        self.backup_obj = models.DJFileBackUp.objects.create(name="Test File Backup", **kwargs)
        self.backup_obj.files.add(self.file_obj.id)
        self.backup_handler = FileBackup(self.backup_obj)

    def test_create_file_backup(self):
        backup_path = self.backup_handler.get_backup()
        self.assertTrue(isinstance(backup_path, Path))

    def test_delete_temp_files(self):
        fb = self.backup_handler
        fb.delete_raw_temp()
        fb.delete_zip_temp()
        delete_item(self._temp_file.name)
        self._temp_file = None


