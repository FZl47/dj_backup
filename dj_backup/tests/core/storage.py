from unittest import mock

from django.test import TestCase

from dj_backup.core import storages
from dj_backup import models


class StorageConnectorImportTests(TestCase):

    @mock.patch('importlib.import_module')
    def test_import_existing_storage_connector(self, mock_import_module):
        mock_module = mock.Mock()
        mock_import_module.return_value = mock_module

        mock_connector = mock.Mock()
        mock_module.LocalStorageConnector = mock_connector

        storages._STORAGES_MODULE['LOCAL'] = ('some.module', 'LocalStorageConnector')

        result = storages.import_storage_connector('LOCAL')

        self.assertEqual(result, mock_connector)
        mock_import_module.assert_called_with('some.module')

    def test_import_unknown_storage(self):
        result = storages.import_storage_connector('UNKNOWN_STORAGE')
        self.assertIsNone(result)

    @mock.patch('importlib.import_module')
    def test_import_storage_connector_missing_attribute(self, mock_import_module):
        mock_module = mock.Mock()
        mock_import_module.return_value = mock_module

        delattr(mock_module, 'MissingConnector')

        storages._STORAGES_MODULE['MISSING'] = ('some.module', 'MissingConnector')

        result = storages.import_storage_connector('MISSING')
        self.assertIsNone(result)


class CheckStoragesConfigTests(TestCase):

    @mock.patch('dj_backup.core.storages.import_storage_connector')
    @mock.patch('dj_backup.settings.get_storages_config')
    def test_check_storages_config_success(self, mock_get_config, mock_import_connector):
        mock_get_config.return_value = {
            'LOCAL': {
                'OUT': '/dj_backup/test'
            },
        }

        class MockConnector:
            config = None
            STORAGE_NAME = 'LOCAL'

            def set_config(self, config):
                self.config = config

            def setup(self):
                pass

            def check(self):
                return True

        mock_import_connector.return_value = MockConnector()

        storages._check_storages_config()

        self.assertIn('LOCAL', storages.ALL_STORAGES_DICT)
        self.assertIn('LOCAL', storages.STORAGES_AVAILABLE_DICT)
        self.assertTrue(any(isinstance(c, MockConnector) for c in storages.STORAGES_CLASSES_CHECKED))


class InitialStoragesObjTests(TestCase):

    @mock.patch('dj_backup.core.storages._check_storages_config')
    @mock.patch('dj_backup.core.storages._reset_storages_state')
    def test_initial_storages_obj_creates_storage(self, mock_reset_state, mock_check_config):
        models.DJStorage.objects.all().delete()
        storages.STORAGES_CLASSES_CHECKED.clear()

        class LocalStorageConnector:
            STORAGE_NAME = 'LOCAL'

        storages.STORAGES_CLASSES_CHECKED.append(LocalStorageConnector)

        storages.initial_storages_obj()

        local_storage = models.DJStorage.objects.filter(name='LOCAL').first()
        self.assertIsNotNone(local_storage)
        self.assertEqual(local_storage.checked, local_storage.storage_class in storages.STORAGES_CLASSES_CHECKED)
