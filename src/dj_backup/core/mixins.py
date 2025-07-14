from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, reverse

from dj_backup.core.storages import load_storage
from dj_backup.models.notification import DJBackupLog


class SuperUserRequiredMixin:
    auth_redirect: bool = False

    def dispatch(self, request, *args, **kwargs) -> None:
        """
            Check if the user is a superuser. If not, redirect or raise PermissionDenied.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Raises:
                PermissionDenied: If the user is not a superuser and auth_redirect is False.

            Returns:
                HttpResponse: Redirects to login page or continues with the request.
        """
        if request.user.is_anonymous or not request.user.is_superuser:
            if self.auth_redirect:
                return redirect(f"{reverse('admin:login')}?next={reverse('dj_backup:dashboard__index')}")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class DJViewMixin(SuperUserRequiredMixin):

    def get_context_data(self, **kwargs) -> dict:
        """
            Get context data with additional notifications count.

            Args:
                **kwargs: Additional keyword arguments.

            Returns:
                dict: The updated context data including notifications count.
        """
        context = super(DJViewMixin, self).get_context_data(**kwargs)
        # add notifications count
        context['notifications_count'] = DJBackupLog.objects.filter(is_seen=False).count()
        return context

    def dispatch(self, request, *args, **kwargs) -> None:
        """
            Load storage before dispatching the request.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                HttpResponse: The response from the superclass dispatch method.
        """
        # load storages
        load_storage()
        return super().dispatch(request, *args, **kwargs)
