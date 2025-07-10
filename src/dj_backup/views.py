from itertools import chain

from django.views.generic import TemplateView, View, ListView, RedirectView
from django.contrib.auth import logout as logout_django
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, Http404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q

from dj_backup.core.backup.db import DATABASES_AVAILABLE
from dj_backup.core import tasks, utils
from dj_backup import models, forms
from dj_backup.core import mixins
from dj_backup import settings


class Login(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('dj_backup:dashboard__index')


class Logout(View):

    def get(self, request):
        logout_django(request)
        return redirect('admin:index')


class Index(mixins.DJViewMixin, TemplateView):
    auth_redirect = True
    template_name = 'dj_backup/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['storages'] = models.DJStorage.objects.all()
        context['file_backups'] = models.DJFileBackUp.objects.all()[:7]
        context['db_backups'] = models.DJDataBaseBackUp.objects.all()[:7]
        return context


class FileList(mixins.DJViewMixin, TemplateView):
    template_name = 'dj_backup/file/list.html'

    def get_context_data(self, **kwargs):
        context = super(FileList, self).get_context_data(**kwargs)
        dir_location = self.request.GET.get('dir')

        base_dirs = settings.get_base_root_dirs()
        if dir_location:
            #  dir path must in base root
            can_access_dir = False
            for base_dir in base_dirs:
                if utils.is_subdirectory(base_dir, dir_location):
                    can_access_dir = True
            if not can_access_dir:
                raise PermissionDenied

            dir_location = [dir_location]
        else:
            dir_location = base_dirs

        files_iter = utils.get_files_dir(*dir_location)

        context.update({
            'files_iter': files_iter,
            'storages': models.DJStorage.objects.all(),
            'enc_types': models.DJBackupSecure.ENCRYPTION_TYPES
        })
        return context


class FileBackupAdd(mixins.DJViewMixin, View):
    form = forms.DJFileBackUpForm
    form_file = forms.DJFileForm
    form_secure = forms.DJBackupSecureForm

    def get_referrer_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request):
        # TODO: MUST refactor this shit
        data = request.POST.copy()
        file_dirs = data.getlist('file_dirs', [])
        if not file_dirs:
            messages.error(request, _('You should set file to backup'))
            return redirect(self.get_referrer_url())
        # create file objs
        file_objects = []
        for file_dir in file_dirs:
            f = self.form_file({
                'dir': file_dir,
                'name': utils.get_file_name(file_dir)
            })
            if not f.is_valid():
                messages.error(request, _('Something went wrong in file object creation'))
                return redirect(self.get_referrer_url())
            file_obj = f.save()
            file_objects.append(file_obj.id)
        data.setlist('files', file_objects)
        f_backup = self.form(data)
        if not f_backup.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_referrer_url())
        backup = f_backup.save()

        # check and create encryption obj
        has_enc = False if data.get('encryption_type', 'none') == 'none' else True
        if has_enc:
            data['backup'] = backup
            f = self.form_secure(data)
            if not f.is_valid():
                backup.delete()
                messages.error(request, _('Please enter fields correctly'))
                return redirect(self.get_referrer_url())
            f.save()

        tasks.ScheduleFileBackupTask(backup)
        messages.success(request, _('Backup file submited successfully'))
        return redirect(self.get_referrer_url())


class DataBaseList(mixins.DJViewMixin, TemplateView):
    template_name = 'dj_backup/db/list.html'

    def get_context_data(self, **kwargs):
        context = super(DataBaseList, self).get_context_data(**kwargs)
        context.update({
            'databases': DATABASES_AVAILABLE,
            'storages': models.DJStorage.objects.all(),
            'enc_types': models.DJBackupSecure.ENCRYPTION_TYPES
        })
        return context


class DataBaseBackupAdd(mixins.DJViewMixin, View):
    form = forms.DJDataBaseBackUpForm
    form_secure = forms.DJBackupSecureForm

    def get_referrer_url(self):
        return self.request.META.get('HTTP_REFERER')

    def post(self, request):
        data = request.POST.copy()
        additional_args = '|'.join(data.getlist('additional_args', []))
        data['additional_args'] = additional_args
        f = self.form(data)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(self.get_referrer_url())
        backup = f.save()

        # check and create encryption obj
        has_enc = False if data.get('encryption_type', 'none') == 'none' else True
        if has_enc:
            data['backup'] = backup
            f = self.form_secure(data)
            if not f.is_valid():
                backup.delete()
                messages.error(request, _('Please enter fields correctly'))
                return redirect(self.get_referrer_url())
            f.save()

        tasks.ScheduleDataBaseBackupTask(backup)
        messages.success(request, _('Backup database submited successfully'))
        return redirect(self.get_referrer_url())


class BackupList(mixins.DJViewMixin, ListView):
    template_name = 'dj_backup/backup/list.html'
    paginate_by = 20

    def search(self, objects):
        search = self.request.GET.get('search')
        if not search:
            return objects
        objects = objects.filter(name__icontains=search)
        return objects

    def get_queryset(self):
        backup_dbs = self.search(models.DJDataBaseBackUp.objects.all())
        backup_files = self.search(models.DJFileBackUp.objects.all())
        qs = list(chain(backup_dbs, backup_files))
        return qs


class BackupDetail(mixins.DJViewMixin, TemplateView):
    template_name = 'dj_backup/backup/detail.html'
    paginate_by_results = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        backup_id = kwargs.get('backup_id')
        backup = models.get_backup_object(backup_id)
        if not backup:
            raise Http404
        context['backup'] = backup
        backup_storages = backup.get_storages()
        for storage in backup_storages:
            storage.usage_size = backup.get_usage_size_by_storage(storage)
            storage.count_backup = backup.get_count_backup_storage(storage)
        context['backup_storages'] = backup_storages
        context['all_storages'] = models.DJStorage.objects.all()
        # paginate results
        results = backup.get_results()
        paginator = Paginator(results, self.paginate_by_results)
        paginator = paginator.get_page(self.request.GET.get('page', 1))
        context['page_obj'] = paginator
        context['results'] = paginator.object_list
        return context


class BackupDelete(mixins.DJViewMixin, View):

    def post(self, request, backup_id):
        backup = models.get_backup_object(backup_id)
        if not backup:
            raise Http404
        backup.delete()
        messages.success(request, _('Backup deleted successfully'))
        return redirect('dj_backup:backup__list')


class BackupUpdate(mixins.DJViewMixin, View):

    def get_form(self, backup):
        data = self.request.POST
        if backup.backup_type == 'database':
            return forms.DJDataBaseBackUpUpdateForm(data, instance=backup)
        else:
            return forms.DJFileBackUpUpdateForm(data, instance=backup)

    def post(self, request, backup_id):
        backup = models.get_backup_object(backup_id)
        if not backup:
            raise Http404

        f = self.get_form(backup)
        if not f.is_valid():
            messages.error(request, _('Please enter fields correctly'))
            return redirect(backup.get_absolute_url())
        backup = f.save()
        # delete old schedule task
        if backup.schedule_task:
            backup.schedule_task.delete()
            # create new task
            tasks.ScheduleFileBackupTask(backup)
        messages.success(request, _('Backup updated successfully'))
        return redirect(backup.get_absolute_url())


class BackupManageRunningStatus(mixins.DJViewMixin, View):

    def post(self, request, backup_id):
        backup = models.get_backup_object(backup_id)
        if not backup:
            raise Http404
        data = request.POST
        status = data.get('status')
        if not status:
            messages.error(request, _('Field status is required'))
            return redirect(backup.get_absolute_url())

        # delete tasks
        backup.delete_tasks()

        if status == 'start':
            if backup.backup_type == 'file':
                tasks.ScheduleFileBackupTask(backup)
            else:
                tasks.ScheduleDataBaseBackupTask(backup)
            messages.success(request, _('Backup status changed to running'))
        else:
            messages.success(request, _('Backup status changed to stopped'))
        return redirect(backup.get_absolute_url())


class DJBackupResultDownload(mixins.DJViewMixin, View):

    def get(self, request, backup_result_id):
        try:
            br = models.DJBackUpStorageResult.objects.get(id=backup_result_id)
        except (models.DJBackUpStorageResult.DoesNotExist, models.DJBackUpStorageResult.MultipleObjectsReturned):
            raise Http404
        local_file = br.get_local_file_path()
        if not local_file:
            raise Http404
        with open(local_file, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename={br.backup_name}'
            return response


class NotificationList(mixins.DJViewMixin, ListView):
    template_name = 'dj_backup/notification/list.html'
    paginate_by = 30

    def search(self, objects):
        search = self.request.GET.get('search')
        if not search:
            return objects
        lookup = Q(level=search) | Q(msg__icontains=search)
        objects = objects.filter(lookup)
        return objects

    def get_queryset(self):
        qs = self.search(models.DJBackupLog.objects.all()).order_by('-created_at', '-is_seen')
        return qs


class NotificationDetail(mixins.DJViewMixin, TemplateView):
    template_name = 'dj_backup/notification/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            notification = models.DJBackupLog.objects.get(id=kwargs['notif_id'])
            notification.is_seen = True
            notification.save(update_fields=['is_seen'])
            context['notif'] = notification
        except models.DJBackupLog.DoesNotExist:
            raise Http404
        return context


class NotificationSeenAll(mixins.DJViewMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('dj_backup:notification__list')

    def get(self, request, *args, **kwargs):
        models.DJBackupLog.objects.filter(is_seen=False).update(is_seen=True)
        return super().get(request, *args, **kwargs)
