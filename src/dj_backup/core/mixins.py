from django.core.exceptions import PermissionDenied


class SuperUserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous or not request.user.is_superuser:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
