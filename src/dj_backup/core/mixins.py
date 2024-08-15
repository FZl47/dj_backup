from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from dj_backup.core import storages, backup


class SuperUserRequiredMixin:
    auth_redirect = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous or not request.user.is_superuser:
            if self.auth_redirect:
                return redirect('admin:index')
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


_init_storages = False


class InitialStoragesMixin:

    def dispatch(self, request, *args, **kwargs):
        global _init_storages
        if not _init_storages:
            storages.get_storages_available()
            _init_storages = True
        return super().dispatch(request, *args, **kwargs)


_init_db_backup = False


class InitialDBBackupMixin:

    def dispatch(self, request, *args, **kwargs):
        global _init_db_backup
        if not _init_db_backup:
            backup.db.get_databases_available()
            _init_db_backup = True
        return super().dispatch(request, *args, **kwargs)


class DJViewMixin(SuperUserRequiredMixin, InitialDBBackupMixin, InitialStoragesMixin):
    pass
