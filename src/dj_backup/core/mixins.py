from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class SuperUserRequiredMixin:
    auth_redirect = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous or not request.user.is_superuser:
            if self.auth_redirect:
                return redirect('admin:index')
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DJViewMixin(SuperUserRequiredMixin):
    pass
