from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, reverse

from dj_backup.core.storages import load_storage


class SuperUserRequiredMixin:
    auth_redirect = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous or not request.user.is_superuser:
            if self.auth_redirect:
                return redirect(f"{reverse('admin:login')}?next={reverse('dj_backup:dashboard__index')}")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DJViewMixin(SuperUserRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        # load storages
        load_storage()
        return super().dispatch(request, *args, **kwargs)
