import abc

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from dj_backup import models


class UserManagement(abc.ABC):
    UserKlass = get_user_model()
    user = None

    def setUp(self):
        # Login user
        self.login()

    def create_user(self):
        user = self.UserKlass.objects.create_superuser(
            username='admin',
        )
        user.set_password('admin')
        user.save()
        self.user = user
        return user

    def get_user(self):
        if self.user:
            return self.user
        return self.create_user()

    def login(self):
        user = self.get_user()
        self.client.force_login(user)


class BackupViewsTests(UserManagement, TestCase):
    storage = None

    def setUp(self):
        super().setUp()

        # Create backup objects
        kwargs = {
            'unit': 'minutes',
            'interval': 1
        }
        models.DJDataBaseBackUp.objects.create(name="Test DB Backup", **kwargs)
        models.DJFileBackUp.objects.create(name="Test File Backup", **kwargs)

        # Create local storage object
        self.storage = models.DJStorage.objects.create(
            **{'name': 'LOCAL', 'display_name': 'Local', 'checked': True},
        )

    def test_backup_list(self):
        url = reverse('dj_backup:backup__list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
